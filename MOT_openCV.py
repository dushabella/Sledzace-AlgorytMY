"""
    Śledzenie pojedycznego lub wielu obiektów na pliku wideo lub obrazie z kamerki
    Wykorzystywana biblioteka OpenCV i wbudowane 7 algorytmów śledzących
    Sposób użycia:
    python3.7 MOT_openCV.py --video nazwapliku.mp4 --tracker algorytm
        s -- wybierz obszar śledzenia (zatwierdź spacją lub enterem)
        q -- zakończ śledzenie i zamknij okno
        c -- anuluj zaznaczenie
    np. python3.7 MOT_openCV.py --video data/pieski.mp4 --tracker mil
"""

from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
from sty import fg, bg, ef, rs

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
	if args["tracker"] not in OPENCV_OBJECT_TRACKERS:
		print("Wybrany algorytm śledzący nie istnieje!")
		exit()
	else:
		# tworzenie specjalnego OpenCV multi-trackera
		trackers = cv2.MultiTracker_create()
	fps = FPS().start()
	return OPENCV_OBJECT_TRACKERS, trackers, fps

def choose_video(args):
	# jeżeli nie została przekazana ścieżka do pliku wideo, obraz brany będzie z kamerki
	if not args.get("video", False):
		print("[INFO] starting video stream...")
		vs = VideoStream(src=0).start()
		time.sleep(1.0)
	# w innym razie - brany jest plik wideo wskazany jako argument
	else:
		vs = cv2.VideoCapture(args["video"])
	return vs

def avg_fps(avg: float, fps: float) -> float:
# counts avg value of fps
    if avg == 0:
        return fps
    else:
        return (avg + fps)/2

def look_ovr_frames(vs, fps, args, OPENCV_OBJECT_TRACKERS, trackers, areas):
	# pętla po klatkach pliku wideo
	av_fps = 0
	while True:
		frame = vs.read()
		frame = frame[1] if args.get("video", False) else frame
		# sprawdzenie czy nie doszliśmy do końca pliku
		if frame is None:
			break
		# zmiana rozmiaru ramki
		frame = imutils.resize(frame, width=500)
		(H, W) = frame.shape[:2]
		# zebranie informacji o bb dla każdego śledzonego obiektu (jeżeli istnieją)
		(success, boxes) = trackers.update(frame)
		# pętla po bounding boxach i wyświetlanie ich na klatce wideo
		for box in boxes:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		# update licznika fps
		fps.update()
		fps.stop()
		av_fps = avg_fps(av_fps, fps.fps())
		# informacje wyświetlane na ekranie
		info = [
		  ("Algorytm", args["tracker"]),
		  ("Sukces", "Tak" if success else "Nie"),
		  ("FPS", "{:.2f}".format(fps.fps())),
		]
		# format i wyświetlanie informacji na ekranie
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 20), 2)
		# wyświetlanie klatki
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break
		elif any(areas):
			for name in areas:
				box = areas[name]
				# utworzenie nowego trackera dla nowego bb i dodanie go do multi-trackera
				tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
				trackers.add(tracker, frame, box)
			areas.clear()


	if (args["video"] == None):
		print(bg.da_magenta, "Koniec testu na obrazie z kamerki śledzonego za pomocą algorytmu ", bg.rs,
			  fg(255, 150, 50), args["tracker"], fg.rs)
	else:
		print(bg.da_magenta, "Koniec testu na filmiku: ", bg.rs, fg(255, 150, 50), args["video"], fg.rs,
			  bg.da_magenta,
			  "śledzonego za pomocą algorytmu", bg.rs, fg(255, 150, 50), args["tracker"], fg.rs)

	if success:
		print(bg.da_cyan, "Średnia wartość klatek przetworzonych na sekundę (fps) wynosiła: ", bg.rs, fg.li_yellow,
			  av_fps, fg.rs)
	else:
		print(bg.da_red, "Śledzenie nie powiodło się!", bg.rs)


def look_ovr_frames_w_selection(vs, fps, args, OPENCV_OBJECT_TRACKERS, trackers):
	# pętla po klatkach pliku wideo
	av_fps = 0
	while True:
		frame = vs.read()
		frame = frame[1] if args.get("video", False) else frame
		# sprawdzenie czy nie doszliśmy do końca pliku
		if frame is None:
			break
		# zmiana rozmiaru ramki
		frame = imutils.resize(frame, width=500)
		(H, W) = frame.shape[:2]
		# zebranie informacji o bb dla każdego śledzonego obiektu (jeżeli istnieją)
		(success, boxes) = trackers.update(frame)
		# pętla po bounding boxach i wyświetlanie ich na klatce wideo
		for box in boxes:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		# update licznika fps
		fps.update()
		fps.stop()
		av_fps = avg_fps(av_fps, fps.fps())
		# informacje wyświetlane na ekranie
		info = [
		  ("Algorytm", args["tracker"]),
		  ("Sukces", "Tak" if success else "Nie"),
		  ("FPS", "{:.2f}".format(fps.fps())),
		]
		# format i wyświetlanie informacji na ekranie
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 20), 2)
		# wyświetlanie klatki
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# jeżeli naciśnięty jest przycisk 's' to będziemy zaznaczać bb do śledzenia
		if key == ord("s"):
			# wybranie obiektu do śledzenia, wybór zatwierdzany SPACJĄ lub ENTEREM
			box = cv2.selectROI("Frame", frame, fromCenter=False,
				showCrosshair=True)
			print("box: ", box)
			# fps = FPS().start()
			# utworzenie nowego trackera dla nowego bb i dodanie go do multi-trackera
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)
		# jeżeli naciśnięty został przycisk 'q' program wyjdzie z pętli
		elif key == ord("q"):
			break

	if (args["video"] == None):
		print(bg.da_magenta, "Koniec testu na obrazie z kamerki śledzonego za pomocą algorytmu ", bg.rs,
			  fg(255, 150, 50), args["tracker"], fg.rs)
	else:
		print(bg.da_magenta, "Koniec testu na filmiku: ", bg.rs, fg(255, 150, 50), args["video"], fg.rs,
			  bg.da_magenta,
			  "śledzonego za pomocą algorytmu", bg.rs, fg(255, 150, 50), args["tracker"], fg.rs)

	if success:
		print(bg.da_cyan, "Średnia wartość klatek przetworzonych na sekundę (fps) wynosiła: ", bg.rs, fg.li_yellow,
			  av_fps, fg.rs)
	else:
		print(bg.da_red, "Śledzenie nie powiodło się!", bg.rs)

def release_pointer(vs, args):
    # przy wykorzystaniu kamerki, uwolnienie wskaźnika
    if not args.get("video", False):
      vs.stop()
    else:
      vs.release()
    # zamknij wszystkie okna
    cv2.destroyAllWindows()



if __name__ == "__main__":

	areas = {
		# pieski.mp4
		"piesek1": (41, 361, 136, 170),
		"piesek2": (201, 362, 165, 154),
		"studzienka": (421, 368, 79, 63)}

	args = arg_parser()
	opencv_trckers, trackers, fps = choose_tracker(args)
	# fps = FPS().start()
	vs = choose_video(args)
	look_ovr_frames_w_selection(vs, fps, args, opencv_trckers, trackers)
	# look_ovr_frames(vs, fps, args, opencv_trckers, trackers, areas)
	release_pointer(vs, args)