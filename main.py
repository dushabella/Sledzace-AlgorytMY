from data_downloader import download_file_from_google_drive as download
import SOT_openCV

videos = {
    "1ObQ1515WzvgusfJOuh7RVs7Bxxesy8kz": "./data/race.mp4",
    "1WU8Xqne-6YcusHtQ9sr2qICrB1K4ysGF": "./data/pieski.mp4",
    "114QEzVWm9FUiy-TAeW0rpAoxvATWuS8W": "./data/nascar_02.mp4",
    "1cCJncXIvddvEzr_BWNPq2dIuc2-IzY6z": "./data/nascar_01.mp4",
    "1icwmORKqh6Lv5GMUN_mzn-IyNg1H4GEM": "./data/drone.mp4",
    "1-9zNexo0RZA3SPQ0q6334QwCWEWsiLO-": "./data/dashcam_boston.mp4",
    "1jKDtfacJ9JnPT18Qvio14jYWa6CV9e7j": "./data/american_pharoah.mp4",
    "1JViJlwpx4IKukwlcuuEMUjpocBg729GW": "./data/pieski2.mp4"
}

areas = {
    # pieski2.mp4
    "pieski_mordka_S": (236, 386, 39, 44),
    "pieski_ogon_M": (107, 359, 64, 59),
    "pieski_caly_L": (179, 346, 201, 190),}

    # # american_pharoah.mp4
    # "american_jezdziec_S": (433, 121, 22, 21),
    # "american_kon_M": (418, 120, 74, 44),
    # "american_zbiorowe_L": (120, 115, 160, 51),
    #
    # # dashcam_boston.mp4
    # "dashcam_swiatla_S": (430, 112, 24, 24),
    # "dashcam_suv_M": (403, 181, 38, 34),
    # "dashcam_honda_L": (317, 177, 64, 60),
    #
    # # drone.mp4
    # "drone_bialy_S": (329, 49, 21, 20),
    # "drone_szary_M": (224, 142, 75, 64),
    # "drone_szary_L": (161, 132, 206, 87),
    #
    # # nascar_01.mp4
    # "nascar1_zielony_S": (250, 123, 37, 23),
    # "nascar1_zielony_M": (240, 115, 57, 41),
    # "nascar_zielony_L": (220, 97, 102, 73),
    #
    # # nascar_02.mp4
    # "nascar2_zielony_S": (208, 169, 40, 45),
    # "nascar2_zielony_M": (200, 166, 62, 60),
    # "nascar2_zielony_L": (187, 146, 97, 93),
    #
    # # race.mp4
    # "race_zawodnik_S": (187, 124, 30, 46),
    # "race_zawodnik_M": (175, 122, 48, 98),
    # "race_zawodnik_L": (168, 119, 73, 115)}

trackers = [
    "csrt",
    "kcf",
    "boosting",
    "mil",
    "tld",
    "medianflow",
    "mosse"]

args = {"video": "data/pieski2.mp4", "tracker": "mil"}

if __name__ == "__main__":

    # update the video files
    for file_id, filename in videos.items():
        download(file_id, filename)

    for tracker in trackers:
        args["tracker"] = tracker
        print(args)
        # run tracking for the particular video
        for name, boundingbox in areas.items():
            tracker = SOT_openCV.choose_tracker(args)
            initBB = None
            vs = SOT_openCV.choose_video(args)
            fps = None

            SOT_openCV.look_ovr_frames(vs, args, initBB, tracker, boundingbox)
            SOT_openCV.release_pointer(vs, args)

    # run tracking for the particular video
    # for name, boundingbox in areas.items():
    #     args = {"video": "data/pieski2.mp4", "tracker": "mil"}
    #     tracker = SOT_openCV.choose_tracker(args)
    #     initBB = None
    #     vs = SOT_openCV.choose_video(args)
    #     fps = None
    #
    #     SOT_openCV.look_ovr_frames(vs, args, initBB, tracker, boundingbox)
    #     SOT_openCV.release_pointer(vs, args)
