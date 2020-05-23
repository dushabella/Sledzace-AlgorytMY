"""
    Compare OpenCV tracking algorithms.
    Usage:
        python3.7 SOT_openCV.py --video data/pieski.mp4 --tracker tracker_version
        s -- select area for tracking
        q -- quit
        c -- cancel the selection
"""

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
def arg_parser():
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", type=str,
	  help="path to input video file")
	ap.add_argument("-t", "--tracker", type=str, default="kcf",
	  help="OpenCV object tracker type")
	args = vars(ap.parse_args())
	return(args)

def choose_tracker(args):
	# extract the OpenCV version info
	(major, minor) = cv2.__version__.split(".")[:2]
	# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
	# function to create our object tracker
	if int(major) == 3 and int(minor) < 3:
	  tracker = cv2.Tracker_create(args["tracker"].upper())
	# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
	# approrpiate object tracker constructor:
	else:
	  # initialize a dictionary that maps strings to their corresponding
	  # OpenCV object tracker implementations
	  OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	  }
	  # grab the appropriate object tracker using our dictionary of
	  # OpenCV object tracker objects
	  tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
	return(tracker)


def choose_video(args):
	# if a video path was not supplied, grab the reference to the web cam
	if not args.get("video", False):
	  print("[INFO] starting video stream...", args)
	  vs = VideoStream(src=0).start()
	  time.sleep(1.0)
	# otherwise, grab a reference to the video file
	else:
	  vs = cv2.VideoCapture(args["video"])
	return(vs)

def define_object(initBB, frame):
    # predefine area for tracking
    tracker.init(frame, initBB)
    fps = FPS().start()
    return(fps)

def look_ovr_frames(vs, args, initBB, areas):
    # loop over frames from the video stream
    while True:
      # grab the current frame, then handle if we are using a
      # VideoStream or VideoCapture object
      frame = vs.read()
      frame = frame[1] if args.get("video", False) else frame
      # check to see if we have reached the end of the stream
      if frame is None:
        break
      # resize the frame (so we can process it faster) and grab the
      # frame dimensions
      frame = imutils.resize(frame, width=500)
      (H, W) = frame.shape[:2]

      # check to see if we are currently tracking an object
      if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
          (x, y, w, h) = [int(v) for v in box]
          cv2.rectangle(frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2)
        # update the FPS counter
        fps.update()
        fps.stop()
        # initialize the set of information we'll be displaying on
        # the frame
        info = [
          ("Tracker", args["tracker"]),
          ("Success", "Yes" if success else "No"),
          ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
          text = "{}: {}".format(k, v)
          cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the output frame
      cv2.imshow("Frame", frame)
      key = cv2.waitKey(1) & 0xFF

      # if the 's' key is selected, we are going to "select" a bounding
      # box to track
      if key == ord("q"):
        break

      # select predefined a bounding box to track
      else:
        initBB = areas
        fps = define_object(initBB, frame)


def look_ovr_frames_w_selection(vs, args, initBB):
    # loop over frames from the video stream
    while True:
      # grab the current frame, then handle if we are using a
      # VideoStream or VideoCapture object
      frame = vs.read()
      frame = frame[1] if args.get("video", False) else frame
      # check to see if we have reached the end of the stream
      if frame is None:
        break
      # resize the frame (so we can process it faster) and grab the
      # frame dimensions
      frame = imutils.resize(frame, width=500)
      (H, W) = frame.shape[:2]

      # check to see if we are currently tracking an object
      if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
          (x, y, w, h) = [int(v) for v in box]
          cv2.rectangle(frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2)
        # update the FPS counter
        fps.update()
        fps.stop()
        # initialize the set of information we'll be displaying on
        # the frame
        info = [
          ("Tracker", args["tracker"]),
          ("Success", "Yes" if success else "No"),
          ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
          text = "{}: {}".format(k, v)
          cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the output frame
      cv2.imshow("Frame", frame)
      key = cv2.waitKey(1) & 0xFF

      # if the 's' key is selected, we are going to "select" a bounding
      # box to track
      if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
          showCrosshair=True)
        print("initBB: ", initBB)
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()

      # if the `q` key was pressed, break from the loop
      elif key == ord("q"):
        break


def release_pointer(vs, args):
    # if we are using a webcam, release the pointer
    if not args.get("video", False):
      vs.stop()
    # otherwise, release the file pointer
    else:
      vs.release()
    # close all windows
    cv2.destroyAllWindows()

args = arg_parser()
tracker = choose_tracker(args)
print("tracker ", tracker)
# initialize the bounding box coordinates of the object we are going to track
initBB = None
vs = choose_video(args)
print("vs: ", vs)
fps = None

areas = {"pieski_mordka_S": (236, 386, 39, 44),
         "pieski_ogon_M":  (107, 359, 64, 59),
         "pieski_caly_L": (179, 346, 201, 190)}

look_ovr_frames(vs, args, initBB, areas["pieski_ogon_M"])
# look_ovr_frames_w_selection(vs, args, initBB)
release_pointer(vs, args)

if __name__ == "__main__":
	print("loleells")
