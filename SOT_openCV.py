"""
    Śledzenie pojedycznego obiektu na pliku wideo lub obrazie z kamerki
    Wykorzystywana biblioteka OpenCV i wbudowane 7 algorytmów śledzących
    Sposób użycia:
    python3.7 cvtrackersot.py --video nazwapliku.mp4 --tracker algorytm
        s -- wybierz obszar śledzenia
        q -- zakończ śledzenie i zamknij okno
        c -- anuluj zaznaczenie
    np. python3.7 SOT_openCV.py --video data/pieski.mp4 --tracker mil
"""

# import wymaganych pakietów
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

# przekazywanie argumentów
def arg_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
      help="path to input video file")
    ap.add_argument("-t", "--tracker", type=str, default="kcf",
      help="OpenCV object tracker type")
    args = vars(ap.parse_args())
    return(args)

def choose_tracker(args):
    # uzyskanie informacji o wersji OpenCV (dla różnych wersji inaczej tworzy się instancje trackerów)
    (major, minor) = cv2.__version__.split(".")[:2]
    # dla wersji OpenCV 3.2 albo niższej
    if int(major) == 3 and int(minor) < 3:
        tracker = cv2.Tracker_create(args["tracker"].upper())
    # dla wersji OpenCV 3.3 lub nowszej należy jawnie odwołać się do kontruktora danego trackera
    else:
    # tworzenie słownika zawierającego nazwy i korespondujące konstruktory
    # lista dostępnych w OpenCV algorytmów śledzących
        OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
        }
        # Wybór danego trackera w zależności od przekazanego argumentu
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
    return(tracker)


def choose_video(args):
    # print("choose - video args[video]: ", args["video"])
    if args.get("video"): # podano ścieżkę do pliku
        return cv2.VideoCapture(args["video"])
    else: # obraz z kamerki
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)
    return vs

def define_object(initBB, frame, tracker):
    tracker.init(frame, initBB)
    # inicjalizacja licznika FPS
    fps = FPS().start()
    return(fps)

def look_ovr_frames(vs, args, initBB, tracker, areas):
    # pętla po klatkach pliku wideo
    while True:
      frame = vs.read()
      frame = frame[1] if args.get("video", False) else frame
      # sprawdzenie czy nie doszliśmy do końca pliku
      if frame is None:
        break
      # zmiana rozmiaru ramki, uzyskanie jej wymiarów
      frame = imutils.resize(frame, width=500)
      (H, W) = frame.shape[:2]

      # sprawdzenie, czy już czegoś nie śledzimy
      if initBB is not None:
        # wzięcie nowego bounding boxa (jego współrzędnych) dla obiektu
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
          (x, y, w, h) = [int(v) for v in box]
          cv2.rectangle(frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2)
        # update licznika fps
        fps.update()
        fps.stop()
        # informacje wyświetlane na ekranie
        info = [
          ("Tracker", args["tracker"]),
          ("Success", "Yes" if success else "No"),
          ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # format i wyświetlanie informacji na ekranie
        for (i, (k, v)) in enumerate(info):
          text = "{}: {}".format(k, v)
          cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # wyświetlanie klatki
      cv2.imshow("Frame", frame)
      key = cv2.waitKey(1) & 0xFF

      # jeżeli naciśnięty został przycisk 'q' program wyjdzie z pętli
      if key == ord("q"):
        break

      # pobierz obszar do śledzenia ze słownika areas
      else:
        initBB = areas
        fps = define_object(initBB, frame, tracker)


def look_ovr_frames_w_selection(vs, args, initBB, tracker):
    # pętla po klatkach pliku wideo
    while True:
      frame = vs.read()
      frame = frame[1] if args.get("video", False) else frame
      # sprawdzenie czy nie doszliśmy do końca pliku
      if frame is None:
        break
      # zmiana rozmiaru ramki, uzyskanie jej wymiarów
      frame = imutils.resize(frame, width=500)
      (H, W) = frame.shape[:2]

      # sprawdzenie, czy już czegoś nie śledzimy
      if initBB is not None:
        # wzięcie nowego bounding boxa (jego współrzędnych) dla obiektu
        (success, box) = tracker.update(frame)
        # sprawdzenie, czy śledzenie powiodło się
        if success:
          (x, y, w, h) = [int(v) for v in box]
          cv2.rectangle(frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2)
        # update licznika fps
        fps.update()
        fps.stop()
        # informacje wyświetlane na ekranie
        info = [
          ("Tracker", args["tracker"]),
          ("Success", "Yes" if success else "No"),
          ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # format i wyświetlanie informacji na ekranie
        for (i, (k, v)) in enumerate(info):
          text = "{}: {}".format(k, v)
          cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

      # wyświetlanie klatki
      cv2.imshow("Frame", frame)
      key = cv2.waitKey(1) & 0xFF

      # jeżeli naciśnięty jest przycisk 's' to będziemy zaznaczać bb do śledzenia
      if key == ord("s"):
        # wybranie obiektu do śledzenia, wybór zatwierdzany SPACJĄ lub ENTEREM
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
          showCrosshair=True)
        print("initBB: ", initBB)
        # rozpoczęcie śledzenia z wybranym bb, rozpoczęcie obliczeń FPS
        tracker.init(frame, initBB)
        fps = FPS().start()

      # jeżeli naciśnięty został przycisk 'q' program wyjdzie z pętli
      elif key == ord("q"):
        break


def release_pointer(vs, args):
    # przy wykorzystaniu kamerki, uwolnienie wskaźnika
    if not args.get("video", False):
      vs.stop()
    else:
      vs.release()
    # zamknij wszystkie okna
    cv2.destroyAllWindows()

"""
    Zbiór współrzędnych initBB dla projektu zespołowego
    Format współrzędnych (x y w h)
"""
# pieski2.mp4
areas = {"pieski_mordka_S": (236, 386, 39, 44),
         "pieski_ogon_M": (107, 359, 64, 59),
         "pieski_caly_L": (179, 346, 201, 190)}

# # american_pharoah.mp4
# areas = {"american_jezdziec_S": (433, 121, 22, 21),
#          "american_kon_M": (418, 120, 74, 44),
#          "american_zbiorowe_L": (120, 115, 160, 51)}
#
# # dashcam_boston.mp4
# areas = {"dashcam_swiatla_S": (430, 112, 24, 24),
#          "dashcam_suv_M": (403, 181, 38, 34),
#          "dashcam_honda_L": (317, 177, 64, 60)}
#
# # drone.mp4
# areas = {"drone_bialy_S": (329, 49, 21, 20),
#          "drone_szary_M": (224, 142, 75, 64),
#          "drone_szary_L": (161, 132, 206, 87)}
#
# # nascar_01.mp4
# areas = {"nascar1_zielony_S": (250, 123, 37, 23),
#          "nascar1_zielony_M": (240, 115, 57, 41),
#          "nascar_zielony_L": (220, 97, 102, 73)}
#
# # nascar_02.mp4
# areas = {"nascar2_zielony_S": (208, 169, 40, 45),
#          "nascar2_zielony_M": (200, 166, 62, 60),
#          "nascar2_zielony_L": (187, 146, 97, 93)}
#
# # race.mp4
# areas = {"race_zawodnik_S": (187, 124, 30, 46),
#          "race_zawodnik_M": (175, 122, 48, 98),
#          "race_zawodnik_L": (168, 119, 73, 115)}

if __name__ == "__main__":
    args = arg_parser()
    tracker = choose_tracker(args)
    # Inicjowanie bounding boxa obiektu, który chcemy śledzić (none ponieważ wybieramy bb poprzez zaznaczenie na ekranie)
    initBB = None
    vs = choose_video(args)
    fps = None

    # look_ovr_frames(vs, args, initBB, tracker, areas["pieski_ogon_M"])
    look_ovr_frames_w_selection(vs, args, initBB, tracker)
    release_pointer(vs, args)
    print("lolells")
