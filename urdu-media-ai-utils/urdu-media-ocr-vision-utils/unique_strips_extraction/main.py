import os
import cv2

from localize_and_get_unique_strips import extract_frames, extract_news_strips, differentiate_news_strips_orb

if __name__ == "__main__":
    video_path = "/home/cle-dl-05/Desktop/ArooshWork/Unique_Strips/TestSet/Zeeshan_Test_video/test.mp4"
    uniques_dir = "/home/cle-dl-05/Desktop/ArooshWork/Unique_Strips/TestSet/Outputs/New_Z/test/uniques"
    if not os.path.exists(uniques_dir):
        os.makedirs(uniques_dir)
    frames = extract_frames(video_path)
    strips = extract_news_strips(frames, "/home/cle-dl-05/Desktop/ArooshWork/Unique_Strips/best.pt")
    unique_strips = differentiate_news_strips_orb(strips)
    for i,strip in enumerate(unique_strips):
        img = strip[-3]
        cv2.imwrite(os.path.join(uniques_dir,"{}.jpg".format(i)), img)
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


