import random
import time
from mido import Message, MidiFile, MidiTrack

mid = MidiFile('gruppa_krovi.mid')
data = []
chans = {}
master_chans = {-1: None}
for i, track in enumerate(mid.tracks):
	print('Track {}: {}'.format(i, track.name))
	for msg in track:
		#print(msg)
		if (msg.type=="program_change"):
			chans[msg.channel]=msg.program
			if not(msg.program in master_chans.keys()):
				master_chans[msg.program] = len(master_chans)-1
		if (msg.type=="note_on") | (msg.type=="note_off"):
			data.append(str(msg.type) + " " + str(chans[msg.channel]) + " " + str(msg.note) + " " + str(msg.velocity) + " " + str(msg.time))
			#time.sleep(0.2)
chans = {}
mid = MidiFile('pachka_sigaret.mid')
for i, track in enumerate(mid.tracks):
	print('Track {}: {}'.format(i, track.name))
	for msg in track:
		#print(msg)
		if (msg.type=="program_change"):
			chans[msg.channel]=msg.program
			if not(msg.program in master_chans.keys()):
				master_chans[msg.program] = len(master_chans)-1
		if (msg.type=="note_on") | (msg.type=="note_off"):
			data.append(str(msg.type) + " " + str(chans[msg.channel]) + " " + str(msg.note) + " " + str(msg.velocity) + " " + str(msg.time))
			#time.sleep(0.2)
#print(master_chans)
order=6
markov_chain={}

for i in range(len(data)-order):
	try:	
		markov_chain[tuple(data[i:i+order])].append(data[i+order])
	except:
		markov_chain[tuple(data[i:i+order])] = [data[i+order]]
count = 0
for i in markov_chain:
	chain_unit={}
	for j in markov_chain[i]:
		try:	
			chain_unit[j]+=1
		except:
			chain_unit[j]=1
	#print(i, markov_chain[i], chain_unit)
	sm = 0
	for j in chain_unit:
		sm+=chain_unit[j]
	for j in chain_unit:
		chain_unit[j] = chain_unit[j]/sm
		if chain_unit[j]<1:
			count+=1
	markov_chain[i]=chain_unit
	#print(i, markov_chain[i], chain_unit)

for i in markov_chain:
	print(i, markov_chain[i])

print(count, str((count/len(markov_chain))*100) + "%" )

mid = MidiFile()
track = MidiTrack()
track_simp = []
mid.tracks.append(track)
for i in chans:
	track.append(Message('program_change', channel=i, program=chans[i], time=0))



track.append(Message("note_on", channel=master_chans[101], note=57, velocity=80, time=960))
track.append(Message("note_on", channel=master_chans[101], note=54, velocity=80, time=0))
track.append(Message("note_on", channel=master_chans[101], note=49, velocity=80, time=0))
track.append(Message("note_off", channel=master_chans[101], note=57, velocity=64, time=960))
track.append(Message("note_off", channel=master_chans[101], note=54, velocity=64, time=0))
track.append(Message("note_off", channel=master_chans[101], note=49, velocity=64, time=0))

track_simp.append("note_on" + " " + str(101) + " " + "57" + " " + "80" + " " + "960")
track_simp.append("note_on" + " " + str(101) + " " + "54" + " " + "80" + " " + "0")
track_simp.append("note_on" + " " + str(101) + " " + "49" + " " + "80" + " " + "0")
track_simp.append("note_off" + " " + str(101) + " " + "57" + " " + "64" + " " + "960")
track_simp.append("note_off" + " " + str(101) + " " + "54" + " " + "64" + " " + "0")
track_simp.append("note_off" + " " + str(101) + " " + "49" + " " + "64" + " " + "0")


for cnt in range(9000):
	#input()
	seed = random.random()
	sm = 0
	#print(tuple(track_simp[len(track_simp)-order:len(track_simp)]), markov_chain[tuple(track_simp[len(track_simp)-order:len(track_simp)])])
	for i in markov_chain[tuple(track_simp[len(track_simp)-order:len(track_simp)])]:
		#print(sm)
		if (sm + markov_chain[tuple(track_simp[len(track_simp)-order:len(track_simp)])][i])>=seed:
			mes = i.split()
			#print(i.split())
			#Здесь надо разобраться с зполнением сообщения из markov_chain вместе с master_chans
			track_simp.append(i)
			track.append(Message(mes[0], channel=master_chans[int(mes[1])], note=int(mes[2]), velocity=int(mes[3]), time=int(mes[4])))
			break
		else:
			sm+=markov_chain[tuple(track_simp[len(track_simp)-order:len(track_simp)])][i]
	print(cnt)
	if (cnt%10)==0:
		mid.save('new_song.mid')
mid.save('new_song.mid')