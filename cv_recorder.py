import cv2 as cv

video = cv.VideoCapture(0)  # 웹캠 켜기
recording = False  # 녹화 상태 변수
center_x, center_y = 20, 20  # recording 원 중심
show_recording = False
img_size = (640, 480)
mosaic_recording = False  # 모자이크 녹화 여부

fourcc = cv.VideoWriter_fourcc(*"XVID")  # 코덱

if video.isOpened():
    fps = 20.0
    wait_mesc = int(1000 / fps)

    while True:
        valid, img = video.read()
        if not valid:
            break

        img = cv.resize(img, img_size)

        # 모자이크 적용
        if mosaic_recording:
            small_img = cv.resize(img, (32, 24), interpolation=cv.INTER_LINEAR)  # 축소
            img = cv.resize(small_img, img_size, interpolation=cv.INTER_NEAREST)  # 확대 (모자이크 효과)

        record_img = img.copy() # 미리 이미지를 카피하여 표시부분 안나오게 하기기

        # 녹화 중 표시
        if show_recording:
            cv.circle(img, (center_x, center_y), radius=10, color=(0, 0, 255), thickness=-1)
            cv.putText(img, "Recording...", (center_x + 15, center_y + 5), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
        # 모자이크 중 표시시
        if mosaic_recording:
            cv.putText(img, "Mosaic Mode: ON", (center_x - 10, center_y + 30), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
        if not mosaic_recording :
            cv.putText(img, "Mosaic Mode: OFF", (center_x - 10, center_y + 30), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

        cv.imshow("RECORD", img)  # 화면 출력

        key = cv.waitKey(wait_mesc)

        if key == 27:  # ESC 종료
            break

        if key == ord(" "):  # 스페이스바: 녹화 시작/중지
            show_recording = not show_recording
            if not recording:
                out = cv.VideoWriter("record.avi", fourcc, fps, img_size, isColor=True)
                recording = True
            else:
                recording = False
                out.release()

        if key == 9:  # Tab 키 (모자이크 모드 ON/OFF)
            if not recording:  # 녹화 중이 아닐 때만 변경 가능
                mosaic_recording = not mosaic_recording

        if recording:
            out.write(record_img) 

    cv.destroyAllWindows()


