from flet import *
import subprocess

current_process = None
process_running = False

def main(page:Page):
    page.title = "Scrcpy GUI"
    page.window_height = 800
    page.window_width = 500
    page.padding = 20

    def check_audio_and_video(e):
        if no_audio.value == True and no_video.value == True:
            page.snack_bar = SnackBar(Text("エラー: 音声・映像両方を無効にすることはできません",color=colors.WHITE), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

    device_list = Dropdown(label="デバイスを選択", options=[],expand=True)

    def scan_devices(e):
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            output = result.stdout

            lines = output.splitlines()
            device_ids = []
            device_list.options.clear()
            for line in lines:
                if line.startswith('List of devices'):
                    continue
                if '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    device_ids.append(device_id)
                    device_list.options.append(dropdown.Option(key=device_id,text=device_id))
                    device_list.update()
        except Exception as e:
            page.snack_bar = SnackBar(Text(f"エラー: {e}",color=colors.WHITE), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
    
    def run_scrcpy(e):
        global current_process
        global process_running

        if device_list.value == None:
            page.snack_bar = SnackBar(Text("エラー: デバイスが選択されていません",color=colors.WHITE), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        if process_running:
            current_process.terminate()
            process_running = False
            return
        
        device_id = device_list.value
        command = ["scrcpy"]

        if device_id:
            command.extend(["-s", device_id])
            if no_video.value == True:
                command.extend(["--no-video"])
            if no_audio.value == True:
                command.extend(["--no-audio"])
            if audio_source.value == "internalaudio":
                command.extend(["--audio-source=output"])
            elif audio_source.value == "mic":
                command.extend(["--audio-source=mic"])
            if video_source.value == "display":
                command.extend(["--video-source=display"])
            elif video_source.value == "camera":
                command.extend(["--video-source=camera"])
            if video_bitrate.value:
                command.extend([f"--video-bit-rate={video_bitrate.value}M"])
            if audio_bitrate.value:
                command.extend([f"--audio-bit-rate={audio_bitrate.value}K"])
            if video_buffer.value:
                command.extend([f"--display-buffer={video_buffer.value}"])
            if audio_buffer.value:
                command.extend([f"--audio-buffer={audio_buffer.value}"])
            if max_fps.value:
                command.extend([f"--max-fps={max_fps.value}"])
            if render_driver:
                command.extend([f"--render-driver={render_driver.value}"])
            
            try:
                run_button.icon = icons.STOP
                run_button.update()
                with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                    current_process = process
                    process_running = True
                    for line in process.stdout:
                        print(line.decode().strip())
                    process.wait()
                    current_process = None
                    process_running = False
                    run_button.icon = icons.PLAY_ARROW
                    run_button.update()
            
            except Exception as e:
                page.snack_bar = SnackBar(Text(f"Error: {e}",color=colors.WHITE), bgcolor=colors.RED)
                page.snack_bar.open = True
                page.update()
                current_process = None
                process_running = False
                run_button.icon = icons.PLAY_ARROW
                run_button.update()
            
            finally:
                current_process = None
                process_running = False
                run_button.icon = icons.PLAY_ARROW
                run_button.update()

    scan_button = ElevatedButton("デバイスをスキャン", on_click=scan_devices)
    # options
    no_video = Checkbox(label="映像なし", value=False,on_change=check_audio_and_video)
    no_audio = Checkbox(label="音声なし", value=False,on_change=check_audio_and_video)
    audio_source = Dropdown(label="音声ソース", options=[dropdown.Option(key="internalaudio",text="内部音声"),dropdown.Option(key="mic",text="マイク")])
    video_source = Dropdown(label="映像ソース", options=[dropdown.Option(key="display",text="ディスプレイ"),dropdown.Option(key="camera",text="カメラ")])
    video_bitrate = TextField(label="映像ビットレート",suffix_text="M",text_align=TextAlign.RIGHT,expand=True,hint_text="4")
    audio_bitrate = TextField(label="音声ビットレート",suffix_text="K",text_align=TextAlign.RIGHT,expand=True,hint_text="128")
    audio_buffer = TextField(label="音声バッファー",suffix_text="ms",expand=True,text_align=TextAlign.RIGHT,hint_text="50")
    video_buffer = TextField(label="映像バッファー",suffix_text="ms",expand=True,text_align=TextAlign.RIGHT,hint_text="0")
    max_fps = TextField(label="最大FPS", suffix_text="fps", text_align=TextAlign.RIGHT, hint_text="60")
    render_driver = Dropdown(label="レンダラードライバ",options=[dropdown.Option(key="direct3d"),dropdown.Option(key="opengl"),dropdown.Option(key="opengles2"),dropdown.Option(key="opengles"),dropdown.Option(key="metal"),dropdown.Option(key="software")])

    run_button = FloatingActionButton(icon=icons.PLAY_ARROW, on_click=run_scrcpy)

    page.add(
        Text("デバイス",size=24),
        Row([
            device_list,
            scan_button
        ]),
        Text("オプション",size=24),
        Row([
            no_video,
            no_audio,
        ]),
        video_source,
        audio_source,
        Row([
            video_bitrate,
            audio_bitrate,
        ]),
        Row([
            video_buffer,
            audio_buffer,
        ]),
        max_fps,
        render_driver,
        run_button
    )

app(target=main)