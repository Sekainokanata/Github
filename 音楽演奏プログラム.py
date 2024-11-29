import numpy as np
import sounddevice as sd
import threading

############MAIN PARAMETER############
BPM = 73
bar_line_second = (60/BPM)*4  # 1小節の秒数
Defalt_Volume = 0.1
sample_rate = 88000  # サンプルレート
phase = 0
current_sound_index = 0
played_frames = 0
durations = []#MAIN CODE
frequencies = []#MAIN CODE
duration_guiter = []#GUITAR CODE
frequencies_guiter = []#GUITAR CODE
#####################################



# 音名と周波数の対応表
frequencies_dict = {
    "BR": 0,  # 休符
    "C2": 65.41,  # ド
    "D2": 73.42,  # レ
    "E2": 82.41,  # ミ
    "F2": 87.31,  # ファ
    "G2": 98.00,  # ソ
    "A2": 110.00,  # ラ
    "B2♭": 116.54,  # シ♭
    "B2": 123.47,  # シ
    "C3": 130.81,  # ド
    "D3": 146.83,  # レ
    "E3": 164.81,  # ミ
    "F3": 174.61,  # ファ
    "F3♯": 185.00,  # ファ♯
    "G3": 196.00,  # ソ
    "A3": 220.00,  # ラ
    "B3♭": 233.08,  # シ♭
    "B3": 246.94,  # シ
    "C4": 261.63,  # ド
    "D4": 293.66,  # レ
    "E4♭": 311.13,  # ミ♭
    "E4": 329.63,  # ミ
    "F4": 349.23,  # ファ
    "G4": 392.00,  # ソ
    "A4": 440.00,  # ラ
    "B4♭": 466.16,  # シ♭
    "B4": 493.88,  # シ
    "C5": 523.25,  # ド
    "D5": 587.33,  # レ
    "E5♭": 622.25,  # ミ♭
    "E5": 659.25,  # ミ
    "F5": 698.46,  # ファ
    "G5": 783.99,  # ソ
}

# コードの周波数リスト
G = [frequencies_dict["G2"], frequencies_dict["B2"], frequencies_dict["D3"]]
C = [frequencies_dict["C3"], frequencies_dict["E3"], frequencies_dict["G3"]]
D = [frequencies_dict["D3"], frequencies_dict["F3♯"], frequencies_dict["A3"]]
B7 = [frequencies_dict["B2"], frequencies_dict["D3"], frequencies_dict["F3♯"], frequencies_dict["A3"]]
Em = [frequencies_dict["E3"], frequencies_dict["G3"], frequencies_dict["B3"]]
Bm = [frequencies_dict["B2"], frequencies_dict["D3"], frequencies_dict["F3♯"]]



###MAIN CODE###
Gakufu1 = ["B3♭","B3♭","B3♭","B3♭","B3♭","F3","F3","B3♭","B3♭","F3","F3","B3♭","C4","BR","B3♭",
          "C4","C4","C4","C4","C4","B3♭","B3♭","C4","D4","E4♭","D4","C4","C4","B3♭",
          "B3♭","B3♭","B3♭","B3♭","B3♭","G4","G4","F4","E4♭","D4","E4♭","D4","BR","F3",
          "C4","C4","C4","C4","C4","D4","D4","E4♭","D4","C4","D4","C4",
          "B3♭","B3♭","B3♭","B3♭","B3♭","F3","F3","B3♭","B3♭","F3","F3","B3♭","C4","BR","B3♭",
          "C4","C4","C4","C4","C4","B3♭","C4","D4","E4♭","D4","C4","B3♭",
          "C4","B3♭","B3♭","A4","B4♭","BR","B3♭","B3♭","C4",
          "D4","C4","C4","B3♭","E4♭","D4","C4","B3♭","B3♭",]

Tempo1 =  [1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,
          1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/8,1/8,(1/16)+(1/32),1/32,1/16,1/16,
          1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,
          1/16,1/16,1/16,1/16,1/8,1/16,1/16,1/16,1/16,1/16,1/16,1/4,
          1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,
          1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/8,1/8,1/8,1/16,1/16,
          1/16,1/8,1/16,(1/8)+(1/16),(1/16)+(1/4),1/16,1/16,1/16,1/16,
          1/8,1/16,(1/16)+(1/8),1/16,(1/16)+(1/8),1/16,(1/16)+(1/16),1/16,(1/16)+(1/2),]
###############

###GUITAR CODE###
Gakufu2 =[G,G,C,C,D,D,B7,B7,Em,Em,Bm,Bm,C,C,D,D,G,G,C,C,D,D,B7,B7,Em,Em,Bm,Bm,C,C,D,D]

Tempo2 = [1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,1/4,]
#################



if Defalt_Volume ==0:
    Volume = float(input("音量を入力してください(0.0~1.0):"))
else:
    Volume = Defalt_Volume

###MAIN CODE###
for i in range(len(Gakufu1)):
    frequencies.append(frequencies_dict[Gakufu1[i]])
for i in range(len(Gakufu1)):
    durations.append(int(bar_line_second * Tempo1[i] * sample_rate))
################

###GUITAR CODE###
for i in range(len(Gakufu2)):
    frequencies_guiter.append(Gakufu2[i])
for i in range(len(Gakufu2)):
    duration_guiter.append(int(bar_line_second * Tempo2[i] * sample_rate))

def play_guitar_tone(frequencies_guiter, duration_guiter):
    wave = np.array([])
    for f, d in zip(frequencies_guiter, duration_guiter):
        t = np.linspace(0, d / sample_rate, int(d), endpoint=False)
        tone = 0
        for f_tanon in f:
            tone += 0.8 * np.sin(2 * np.pi * f_tanon * t)
            tone += 0.4 * np.sin(2 * np.pi * f_tanon * 2 * t)
            tone += 0.2 * np.sin(2 * np.pi * f_tanon * 3 * t)
        envelope = np.exp(-3 * t)
        tone *= envelope
        wave = np.concatenate((wave, tone))
    wave = wave / np.max(np.abs(wave))
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

# ギターの音を別スレッドで再生
guitar_thread = threading.Thread(target=play_guitar_tone, args=(frequencies_guiter, duration_guiter))
guitar_thread.start()

def generate_wave(frequency, frames, phase, sample_rate):
    # 時間軸の生成
    t = (np.arange(frames) + phase) / sample_rate
    # 信号の生成
    wave = Volume * np.sign(np.sin(2 * np.pi * frequency * t)) # 方形波
    #wave = Volume * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1# 三角波
    #wave = Volume * np.sin(2 * np.pi * frequency * t)# 正弦波
    #wave = Volume * (2 * (t * frequency - np.floor(t * frequency + 0.5)))# ノコギリ波
    return wave

def apply_fade(wave, fade_in_frames, fade_out_frames):
    fade_in = np.linspace(0, 1, fade_in_frames)
    fade_out = np.linspace(1, 0, fade_out_frames)
    wave[:fade_in_frames] *= fade_in
    wave[-fade_out_frames:] *= fade_out
    return wave    

# すべての信号を生成
signals = []
fade_in_frames = int(sample_rate * 0.005)  # フェードインのフレーム数（0.01秒）
fade_out_frames = int(sample_rate * 0.005)  # フェードアウトのフレーム数（0.01秒）

for i in range(len(Gakufu1)):

    frames = durations[i]
    frequency = frequencies[i]
    

    signal = generate_wave(frequency, frames, 0, sample_rate)

    signal = apply_fade(signal, fade_in_frames, fade_out_frames)
    signals.append(signal)

# すべての信号を結合
full_signal = np.concatenate(signals)

def audio_callback(outdata, frames, time, status):
    global played_frames

    if status:
        print(status, flush=True)

    # 再生するフレーム数を決定
    frames_to_play = min(frames, len(full_signal) - played_frames)

    outdata[:frames_to_play] = full_signal[played_frames:played_frames + frames_to_play].reshape(-1, 1)

    # バッファの残り部分をゼロ埋め
    if frames_to_play < frames:
        outdata[frames_to_play:] = 0

    # 再生済みフレームを更新
    played_frames += frames_to_play

def play_square_wave():
    global played_frames
    played_frames = 0

    with sd.OutputStream(channels=1, callback=audio_callback, samplerate=sample_rate):
        print("音声再生中...")
        total_duration = len(full_signal) / sample_rate
        sd.sleep(int(total_duration * 1000))  # 全体の再生が終わるまで待つ
    print("再生終了！")

play_square_wave()