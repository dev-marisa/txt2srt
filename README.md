# txt2srt

Convert Zoom transcripts to usable `srt` formatted subtitles

### What it does

Starting with a transcript that looks like...
```
13:55:12 Hello, this is an example caption! 
13:55:18 Yeah!
...
```

End up with subtitles that look like...
```
1
00:00:01,00 --> 00:00:06,00
Hello, this is an example caption! 

2
00:00:06,00 --> 00:00:08,00
Yeah!
```

### How to use it

Install the file somewhere in your path, then call it from the folder containing the transcript

```
txt2srt closed_caption.txt
```