from data_downloader import download_file_from_google_drive as download
import SOT_openCV

if __name__ == "__main__":
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

    for file_id, filename in videos.items():
        download(file_id, filename)

    argss = {"video": "data/pieski2.mp4", "tracker": "boosting"}
    tracker = SOT_openCV.choose_tracker(argss)
    initBB = None
    vs = SOT_openCV.choose_video(argss)
    fps = None

    areas = {"pieski_mordka_S": (236, 386, 39, 44),
             "pieski_ogon_M":  (107, 359, 64, 59),
             "pieski_caly_L": (179, 346, 201, 190)}

    SOT_openCV.look_ovr_frames(vs, argss, initBB, tracker, areas["pieski_ogon_M"])
    SOT_openCV.release_pointer(vs, argss)
