from data_downloader import download_file_from_google_drive as download
import SOT_openCV
import MOT_openCV
import os
from typing import List, Dict
import copy

def create_dir(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def run_sot_on_video(trackers: List, video: str, areas: Dict) -> None:
# run tracking for the particular video
    args = dict()
    args["video"] = video
    for tracker in trackers:
        args["tracker"] = tracker
        print(tracker)
        for name, boundingbox in areas.items():
            tracker = SOT_openCV.choose_tracker(args)
            initBB = None
            vs = SOT_openCV.choose_video(args)
            fps = None

            SOT_openCV.look_ovr_frames(vs, args, initBB, tracker, boundingbox)
            SOT_openCV.release_pointer(vs, args)

def run_mot_on_video(trackers: List, video: str, areas: Dict) -> None:
# run tracking for the particular video
    args = dict()
    areas_temp = dict()
    args["video"] = video
    areas_temp = copy.deepcopy(areas)
    for tracker in trackers:
        args["tracker"] = tracker
        print(tracker)

        opencv_trckers, trackers, fps = MOT_openCV.choose_tracker(args)
        vs = MOT_openCV.choose_video(args)
        MOT_openCV.look_ovr_frames(vs, fps, args, opencv_trckers, trackers, areas)
        areas = dict(areas_temp.items())
        MOT_openCV.release_pointer(vs, args)


videos = {
    "1ObQ1515WzvgusfJOuh7RVs7Bxxesy8kz": "./data/race.mp4",
    "114QEzVWm9FUiy-TAeW0rpAoxvATWuS8W": "./data/nascar_02.mp4",
    "1cCJncXIvddvEzr_BWNPq2dIuc2-IzY6z": "./data/nascar_01.mp4",
    "1icwmORKqh6Lv5GMUN_mzn-IyNg1H4GEM": "./data/drone.mp4",
    "1-9zNexo0RZA3SPQ0q6334QwCWEWsiLO-": "./data/dashcam_boston.mp4",
    "1jKDtfacJ9JnPT18Qvio14jYWa6CV9e7j": "./data/american_pharoah.mp4",
    "1JViJlwpx4IKukwlcuuEMUjpocBg729GW": "./data/pieski.mp4"
}

""" Areas for SOT testing"""
areas1 = {
    # pieski.mp4
    "pieski_mordka_S": (236, 386, 39, 44),
    "pieski_ogon_M": (107, 359, 64, 59),
    "pieski_caly_L": (179, 346, 201, 190)}

areas2 = {
    # american_pharoah.mp4
    "american_jezdziec_S": (433, 121, 22, 21),
    "american_kon_M": (418, 120, 74, 44),
    "american_zbiorowe_L": (120, 115, 160, 51)}

areas3 = {
    # dashcam_boston.mp4
    "dashcam_swiatla_S": (430, 112, 24, 24),
    "dashcam_suv_M": (403, 181, 38, 34),
    "dashcam_honda_L": (317, 177, 64, 60)}

areas4 = {
    # drone.mp4
    "drone_bialy_S": (329, 49, 21, 20),
    "drone_szary_M": (224, 142, 75, 64),
    "drone_szary_L": (161, 132, 206, 87)}

areas5 = {
    # nascar_01.mp4
    "nascar1_zielony_S": (250, 123, 37, 23),
    "nascar1_zielony_M": (240, 115, 57, 41),
    "nascar_zielony_L": (220, 97, 102, 73)}

areas6 = {
    # nascar_02.mp4
    "nascar2_zielony_S": (208, 169, 40, 45),
    "nascar2_zielony_M": (200, 166, 62, 60),
    "nascar2_zielony_L": (187, 146, 97, 93)}

areas7 = {
    # race.mp4
    "race_usain_bolt": (251, 96, 49, 81),
    "race_tyson_gay": (207, 95, 42, 86),
    "race_asafa_powell": (152, 104, 59, 88)}


""" Areas for MOT testing"""
areas_MOT_1 = {
    # pieski.mp4
    "piesek1": (41, 361, 136, 170),
    "piesek2": (201, 362, 165, 154),
    "studzienka": (421, 368, 79, 63)}

areas_MOT_2 = {
    # race.mp4
    "race_usain_bolt": (251, 96, 49, 81),
    "race_asafa_powell": (152, 104, 59, 88)}

areas_MOT_3 = { # Michał
    # pieski.mp4
    "piesek1": (91, 410, 40, 37),
    "piesek2": (236, 388, 42, 40),
    "studzienka": (424, 391, 75, 24)}

areas_MOT_4 = { # Michał
    # drone.mp4
    "auto1": (187, 111, 60, 53),
	"auto2": (273, 36, 18, 12)}

areas_MOT_5 = { # Michał
    # nascar_01.mp4
    "auto1": (197, 102, 37, 21),
    "auto2": (309, 135, 38, 17)}

areas_MOT_6 = { # Michał
    # race.mp4
    "biegacz1": (206, 103, 41, 75),
    "biegacz2": (257, 99, 34, 82)}


trackers = [
    "csrt",
    "kcf",
    "boosting",
    "mil",
    "tld",
    "medianflow",
    "mosse"]


if __name__ == "__main__":

    create_dir("data")

    # update the video files
    for file_id, filename in videos.items():
        download(file_id, filename)

    """
        TUTAJ ODPALANIE SOT (odkomentować potrzebne)
        Uwaga, można POSIEDZIEĆ I DOPASOWAĆ LEPIEJ TE OBSZARY ŚLEDZENIA 
        robi się to odpalając plik SOT_openCV.py z konsoli i tam po zaznaczeniu obszaru 
        na samym początku filmiku za pomocą "s" i zatwierdzenia go enterem/spacją wypisze się 
        na konsoli initBB w postaci (x, y, h, w) i oczywiście przeklejając do areas
    """
    # run_sot_on_video(trackers, 'data/pieski.mp4', areas1)
    # run_sot_on_video(trackers, 'data/american_pharoah.mp4', areas2)
    # run_sot_on_video(trackers, 'data/dashcam_boston.mp4', areas3)
    # run_sot_on_video(trackers, 'data/drone.mp4', areas4)
    # run_sot_on_video(trackers, 'data/nascar_01.mp4', areas5)
    # run_sot_on_video(trackers, 'data/nascar_02.mp4', areas6)
    # run_sot_on_video(trackers, 'data/race.mp4', areas7)

    """
        TUTAJ ODPALANIE MOT 
    """
    # run_mot_on_video(trackers, 'data/pieski.mp4', areas_MOT_1)
    # run_mot_on_video(trackers, 'data/race.mp4', areas_MOT_2)
    # run_mot_on_video(trackers, 'data/pieski.mp4', areas_MOT_3)
    # run_mot_on_video(trackers, 'data/drone.mp4', areas_MOT_4)
    # run_mot_on_video(trackers, 'data/nascar_01.mp4', areas_MOT_5)
    run_mot_on_video(trackers, 'data/race.mp4', areas_MOT_6)