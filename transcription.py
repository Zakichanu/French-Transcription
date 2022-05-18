## Importing libraries
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def getVideoToWav(videoname: str):
    com1 = f"ffmpeg -i {videoname} video.mp3"
    com2 = "ffmpeg -i video.mp3 -f segment -segment_time 300 -c copy audio_chunks/chunk%03d.wav"
    os.system(com1)
    os.system(com2)

def wav2ytext(language="fr-FR"):
    r = sr.Recognizer()
    with sr.AudioFile("video.wav") as source:
        audio=r.record(source)
        print("Transcription: "+r.recognize_google(audio, language=language))

getVideoToWav("temoignage.mp4")
##wav2ytext("fr-FR")


def silencebasedconversion(path: str):
    song = AudioSegment.from_wav(path)
    fh = open("recognized.txt", "w+")
    print("Processing chunk "+path)

    chunks = split_on_silence(song, min_silence_len = 1000, silence_thresh = -32)
    try:
        os.mkdir(path+'_audio_chunks')
    except(FileExistsError):
        pass
    os.chdir(path+'_audio_chunks')
    i = 0
    for ck in chunks:
        chunksilent = AudioSegment.silent(duration = 100)
        audio_chunk = chunksilent + ck+ chunksilent
        print("saving chunk{0}.wav".format(i))
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav", )
        filename = 'chunk'+str(i)+'.wav'
        print("Processing chunk "+str(i))
        file = filename
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
                    audio_listened = r.listen(source)
        try:
            rec = r.recognize_google(audio_listened, language="fr-FR")
            fh.write(rec+". ")
        except sr.UnknownValueError:
            print("Audio is not understandable")
        except sr.RequestError as e:
            print("Could not request results. check the internet connection")
        i += 1
        os.chdir('..')



list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join("audio_chunks", x)), os.listdir("audio_chunks") ) )
os.chdir("audio_chunks")
##for f in list_of_files:
  ##  silencebasedconversion(f)
