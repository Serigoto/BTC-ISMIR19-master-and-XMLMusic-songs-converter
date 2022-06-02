import math
import os
from email import message
from email.policy import default
from pyexpat.errors import XML_ERROR_UNKNOWN_ENCODING
from statistics import harmonic_mean
import xml.etree.cElementTree as xml
import argparse
import subprocess
import re
import math
from datetime import date

def repetitions(s): #Detecta repeticiones en la canción ya tratada
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))

def initial_file_reading(argBPM, minChordDuration, nombre): #Lee el fichero que genera el BTC y añade la variable de erealpro
                                            #Elimina los acordes residuales y añade variable del loops
    file = open('./Proyecto/Acordes/'+nombre+'.lab', 'r')
    fileResult = open('./Proyecto/Transicion/exampleTransition.lab', 'w')
    lines = file.readlines()
    duracionMinima = minChordDuration
    bpm = argBPM
    spm = 60/bpm
    spmT = spm
    erealpro = 768
    erealproT = erealpro
    desviacion = spm/2

    for index, line in enumerate(lines):
        aux = line.split()
        duracion = round(float(aux[1]) - float(aux[0]),3)
        letra = aux[2]
        if duracion > duracionMinima:
            spmT = spm
            erealproT = erealpro
            while not math.isclose(spmT, duracion, abs_tol=desviacion):
                spmT +=spm
                erealproT += erealpro
            line = str(aux[0]) + ' ' + str(aux[1]) + ' ' +letra +' '+ str(duracion) + ' ' +str(erealproT) + ' ' + str(0)+ ' ' + str(0)
            fileResult.write(line+'\n')
    file.close()
    fileResult.close()

def detection_loop_strings(): #Detecta los bucles en la canción
    file = open('./Proyecto/Transicion/exampleCompleto.lab', 'r')
    lines = file.readlines()
    cadena = ''
    for index, line in enumerate(lines):
        aux = line.split()
        cadena += aux[2]
    file.close()
    return cadena

def loop_delete(cadena): #Elimina los bucles del string cadena
    file = open('./Proyecto/Transicion/exampleCompleto.lab', 'r')
    fileResult = open('./Proyecto/Transicion/exampleAuxiliar.lab','w')
    lines = file.readlines()
    cont = 0
    cont2 = 0
    contGlobal = 1
    buffer = []
    buffer2 = []
    #cadena = cadena.replace(':min','')
    for index, line in enumerate(lines):
        longitud = len(cadena)
        aux = line.split()
        chord = aux[2].replace(':min','')
        if cont != len(cadena):
            cont2 = 0
            if cadena[cont] == chord and aux[5]=='0':
                cont += 1
                buffer2.append(line) 
            else:
                cont = 0
                if buffer2:
                    for i in buffer2:       
                        fileResult.write(i)
                    buffer2 = []
                if cadena[cont] == chord and aux[5]=='0':
                    cont += 1
                    buffer2.append(line)
                else:
                    fileResult.write(line)
        else:
            if cont2 != len(cadena):
                if cadena[cont2] == chord and aux[5]=='0':
                    cont2 += 1
                    buffer.append(line)
                else:
                    cont2 = 0
                    for i in buffer2:       
                        aux = i.split()
                        if contGlobal > 1 : 
                            aux[5] = str(contGlobal)
                        else: 
                            aux[5] = '0'
                            longitud = 0
                        data = aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+aux[4]+' '+ aux[5]+' '+ str(longitud)+'\n'
                        fileResult.write(data)
                    contGlobal=1
                    buffer2 = []
                    for i in buffer:       
                        fileResult.write(i)
                    buffer = []
                    cont = 0
                    if cadena[cont] == chord and aux[5]=='0':
                        cont += 1
                        buffer2.append(line)
                    else:
                        fileResult.write(line)
            else:
                contGlobal += 1
                cont2 = 0
                buffer = []
                if cadena[cont2] == chord and aux[5]=='0':
                    cont2 = 1
                    buffer.append(line)
                else:
                    cont = 0
                    for i in buffer2: 
                        aux = i.split()
                        aux[5] = str(contGlobal)
                        data = aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+aux[4]+' '+ aux[5]+' '+ str(longitud)+'\n'
                        fileResult.write(data)
                    buffer2 = []
                    contGlobal=1
                    fileResult.write(line)
    fileResult.close()
    file.close()

    file = open('./Proyecto/Transicion/exampleAuxiliar.lab', 'r')
    fileResult = open('./Proyecto/Transicion/exampleCompleto.lab','w')
    lines = file.readlines()
    for index, line in enumerate(lines):
        fileResult.write(line)
    fileResult.close()
    file.close()

def loop_election(): #Escoge los bucles repetidos con mayor tamaño
    chordList=(list(repetitions(detection_loop_strings())))
    elegidos = []
    size = 0
    for i in chordList:
        cadena = i[0].replace(':min','')
        if len(cadena) == size:
            elegidos.append(cadena)
        elif len(cadena) > size:
            elegidos = []
            elegidos.append(cadena)
            size = len(cadena) 
    return set(elegidos)#Elimina duplicados

def file_processing():   #Quita los acordes iguales que están seguidos y suma las duraciones
    file = open('./Proyecto/Transicion/exampleTransition.lab', 'r')
    fileResult = open('./Proyecto/Transicion/exampleCompleto.lab','w')
    chord = 'Z'
    prechord = 'X'
    mod = 0
    flag = False
    lines = file.readlines()
    for index, line in enumerate(lines):
        chord = line.split()
        if index != 0:
            if prechord[2] == chord[2]:
                mod = float(chord[3]) + float(prechord[3])
                prechord = chord
                flag = True
            else:
                if flag:
                    flag = False
                    line = str(prechord[0]) + ' ' + str(prechord[1]) + ' ' +prechord[2] +' '+ str(mod) + ' ' +prechord[4]+ ' ' +prechord[5]+ ' ' +prechord[6]
                else : 
                    line = str(prechord[0]) + ' ' + str(prechord[1]) + ' ' +prechord[2] +' '+ prechord[3] + ' ' +prechord[4]+ ' ' +prechord[5]+ ' ' +prechord[6]
                prechord = chord
                fileResult.write(line+'\n')
        else :
            prechord = chord
    line = str(chord[0]) + ' ' + chord[1] + ' ' +chord[2] +' '+ chord[3] + ' ' +chord[4] + ' ' +chord[5]+ ' ' +chord[6]
    fileResult.write(line+'\n')
    fileResult.close()
    file.close()

def generate_XML(fileName, bpm, nombre):  #Lee el fichero de acordes tratado y crea el XML
    score_partwise = xml.Element("score-partwise",version="2.0")
    movement_title = xml.SubElement(score_partwise,'movement-title').text = nombre
    identification = xml.SubElement(score_partwise,'identification')
    creator = xml.SubElement(identification,'creator',type = 'lyricst').text =  str(bpm)
    rights = xml.SubElement(identification,'rights').text =  'Made with Transcriptor Automático'
    encoding = xml.SubElement(identification,'encoding')
    software = xml.SubElement(encoding,'software').text = 'Transcriptor Automático'
    encoding_date = xml.SubElement(encoding,'encoding-date').text = str(date.today())
    supports1 = xml.SubElement(encoding,'supports',element = 'accidental',type = 'no')
    supports2 = xml.SubElement(encoding,'supports',element = 'beam',type = 'no')
    supports3 = xml.SubElement(encoding,'supports',element = 'print',attribute = 'new-page',type = 'yes',value = 'yes')
    supports4 = xml.SubElement(encoding,'supports',element = 'print',attribute = 'new-system',type = 'yes',value = 'yes')

    defaults = xml.SubElement(score_partwise,'defaults')
    scaling = xml.SubElement(defaults,'scaling')
    millimeters = xml.SubElement(scaling,'millimeters').text = '7'
    tenths = xml.SubElement(scaling,'tenths').text = '40'
    page_layout = xml.SubElement(defaults,'page-layout')
    page_height = xml.SubElement(page_layout,'page-height').text = '1700'
    page_width = xml.SubElement(page_layout,'page-width').text = '1200'
    page_margins = xml.SubElement(page_layout,'page-margins',type = 'both')
    left_margin = xml.SubElement(page_margins,'left-margin').text = '72'
    right_margin = xml.SubElement(page_margins,'right-margin').text = '72'
    top_margin = xml.SubElement(page_margins,'top-margin').text = '72'
    bottom_margin = xml.SubElement(page_margins,'bottom-margin').text = '72'

    system_layout = xml.SubElement(defaults,'system-layout')
    system_margins = xml.SubElement(system_layout,'system-margins')
    left_margin = xml.SubElement(system_margins,'left-margin').text = '22'
    right_margin = xml.SubElement(system_margins,'right-margin').text = '0'
    system_distance = xml.SubElement(system_layout,'system-distance').text = '100'
    top_system_distance = xml.SubElement(system_layout,'top-system-distance').text = '73'
    appearance = xml.SubElement(defaults, 'appearance')
    line_width = xml.SubElement(appearance,'line-width', type = 'heavy barline').text = '5'
    line_width = xml.SubElement(appearance,'line-width', type = 'leger').text = '1.5625'
    line_width = xml.SubElement(appearance,'line-width', type = 'light barlin').text = '2.1875'
    line_width = xml.SubElement(appearance,'line-width', type = 'slur middle').text = '0.625'
    line_width = xml.SubElement(appearance,'line-width',type = 'slur tip').text = '0.9375'
    line_width = xml.SubElement(appearance,'line-width',type = 'staff').text = '0.9375'
    line_width = xml.SubElement(appearance,'line-width',type = 'tie middle').text = '2.1875'
    line_width = xml.SubElement(appearance,'line-width',type = 'tie tip').text = '0.625'
    note_size = xml.SubElement(appearance,'note-size',type = 'grace').text = '60'
    note_size = xml.SubElement(appearance,'note-size',type = 'cue').text = '75'
    part_list = xml.SubElement(score_partwise, 'part-list')
    score_part = xml.SubElement(part_list, 'score-part',id = 'P1')
    part_name = xml.SubElement(score_part, 'part-name').text = 'Lead sheet'

    part = xml.SubElement(score_partwise, 'part', id = 'P1')
    measure = xml.SubElement(part, 'measure',number = '1')

    attributes = xml.SubElement(measure,'attributes')
    divisions = xml.SubElement(attributes,'divisions').text ='768'
    time = xml.SubElement(attributes, 'time')
    beats = xml.SubElement(time, 'beats').text = '4'
    beat_type = xml.SubElement(time, 'beat-type').text = '4'
    clef = xml.SubElement(attributes,'clef')
    sign = xml.SubElement(clef, 'sign').text = 'G'
    line = xml.SubElement(clef, 'line').text = '2'

    #LECTURA DEL FICHERO PARA COMPLETAR EL XML
    duracion = 0
    num= 1
    flag = False
    file = open('./Proyecto/Transicion/exampleCompleto.lab', 'r')
    lines = file.readlines()
    cont = 0
    for index2, line1 in enumerate(lines):
        alteracion = 0
        tonalidad = 'major'
        aux = line1.split()
        if aux[6] != '0':
            cont+=1
        else:
            cont= 0
        if ':min' in aux[2]:
            aux[2] = aux[2].replace(':min','')
            tonalidad = 'minor'
        if '#' in aux[2]:
            aux[2] = aux[2].replace('#','')
            alteracion = 1

        if aux[2] != 'N':
            if duracion >= 3072:
                duracion = duracion - 3072 + int (aux[4])
                num += 1
                measure =xml.SubElement(part,'measure',number = str(num))
                if aux[5] != '0' and flag == False and cont != int(aux[6]):
                    flag = True
                    cont = 0
                    direction = xml.SubElement(measure,'direction', placement='above')
                    direction_type = xml.SubElement(direction, 'direction-type')
                    words = xml.SubElement(direction_type,'words').text = str(aux[5]+'x')
                    barline = xml.SubElement(measure, 'barline',location="left")
                    bar_style = xml.SubElement(barline,'bar-style').text = 'heavy-light'
                    repeat = xml.SubElement(barline,'repeat',direction="forward")
                if cont == int(aux[6])-1 and flag:
                    flag = False
                    cont = 0
                    barline = xml.SubElement(measure, 'barline',location="right")
                    bar_style = xml.SubElement(barline,'bar-style').text = 'light-heavy'
                    repeat = xml.SubElement(barline,'repeat',direction="backward")

                harmony = xml.SubElement(measure, 'harmony')
                root = xml.SubElement(harmony, 'root')
                root_step = xml.SubElement(root, 'root-step').text = aux[2]
                root_alter = xml.SubElement(root, 'root-alter').text = str(alteracion)
                kind = xml.SubElement(harmony, 'kind').text = tonalidad
                note = xml.SubElement(measure, 'note')
                pitch = xml.SubElement(note, 'pitch')
                step = xml.SubElement(pitch, 'step').text = 'B'
                octave = xml.SubElement(pitch, 'octave').text = '4'
                if duracion > 3072:
                    duracion = duracion
                    duration = xml.SubElement(note, 'duration').text = str(duracion)
                    duracion = duracion + int(aux[4]) - 3072
                    num +=1
                    measure =xml.SubElement(part,'measure',number = str(num))
                    if aux[5] !='0' and flag == False and cont != int(aux[6]):
                        flag = True
                        cont = 0
                        direction = xml.SubElement(measure,'direction', placement='above')
                        direction_type = xml.SubElement(direction, 'direction-type')
                        words = xml.SubElement(direction_type,'words').text = str(aux[5]+'x')
                        barline = xml.SubElement(measure, 'barline',location="left")
                        bar_style = xml.SubElement(barline,'bar-style').text = 'heavy-light'
                        repeat = xml.SubElement(barline,'repeat',direction="forward")
                    if cont == int(aux[6])-1 and flag:
                        flag = False
                        cont = 0
                        barline = xml.SubElement(measure, 'barline',location="right")
                        bar_style = xml.SubElement(barline,'bar-style').text = 'light-heavy'
                        repeat = xml.SubElement(barline,'repeat',direction="backward")

                    harmony = xml.SubElement(measure, 'harmony')
                    root = xml.SubElement(harmony, 'root')
                    root_step = xml.SubElement(root, 'root-step').text = aux[2]
                    root_alter = xml.SubElement(root, 'root-alter').text = str(alteracion)
                    kind = xml.SubElement(harmony, 'kind').text = tonalidad
                    note = xml.SubElement(measure, 'note')
                    pitch = xml.SubElement(note, 'pitch')
                    step = xml.SubElement(pitch, 'step').text = 'B'
                    octave = xml.SubElement(pitch, 'octave').text = '4'
                    duration = xml.SubElement(note, 'duration').text = aux[4]
                else: 
                    duration = xml.SubElement(note, 'duration').text = aux[4]
            else:
                if aux[5] != '0' and flag == False and cont != int(aux[6]):
                    flag = True
                    cont = 0
                    direction = xml.SubElement(measure,'direction', placement='above')
                    direction_type = xml.SubElement(direction, 'direction-type')
                    words = xml.SubElement(direction_type,'words').text = str(aux[5]+'x')
                    barline = xml.SubElement(measure, 'barline',location="left")
                    bar_style = xml.SubElement(barline,'bar-style').text = 'heavy-light'
                    repeat = xml.SubElement(barline,'repeat',direction="forward")
                if cont == int(aux[6])-1 and flag:
                    flag = False
                    cont = 0
                    barline = xml.SubElement(measure, 'barline',location="right")
                    bar_style = xml.SubElement(barline,'bar-style').text = 'light-heavy'
                    repeat = xml.SubElement(barline,'repeat',direction="backward")

                harmony = xml.SubElement(measure, 'harmony')
                root = xml.SubElement(harmony, 'root')
                root_step = xml.SubElement(root, 'root-step').text = aux[2]
                root_alter = xml.SubElement(root, 'root-alter').text = str(alteracion)
                kind = xml.SubElement(harmony, 'kind').text = tonalidad
                note = xml.SubElement(measure, 'note')
                pitch = xml.SubElement(note, 'pitch')
                step = xml.SubElement(pitch, 'step').text = 'B'
                octave = xml.SubElement(pitch, 'octave').text = '4'
                    
                if duracion +int(aux[4]) > 3072:
                    resto = 3072 -duracion
                    duration = xml.SubElement(note, 'duration').text = str(resto)
                    duracion = int(aux[4]) - resto
                    num +=1
                    measure =xml.SubElement(part,'measure',number = str(num))
                    harmony = xml.SubElement(measure, 'harmony')
                    root = xml.SubElement(harmony, 'root')
                    root_step = xml.SubElement(root, 'root-step').text = aux[2]
                    root_alter = xml.SubElement(root, 'root-alter').text = str(alteracion)
                    kind = xml.SubElement(harmony, 'kind').text = tonalidad
                    note = xml.SubElement(measure, 'note')
                    pitch = xml.SubElement(note, 'pitch')
                    step = xml.SubElement(pitch, 'step').text = 'B'
                    octave = xml.SubElement(pitch, 'octave').text = '4'
                    duration = xml.SubElement(note, 'duration').text = str(duracion)
                else: 
                    duration = xml.SubElement(note, 'duration').text = aux[4]
                    duracion +=int(aux[4])
    barline = xml.SubElement(measure, 'barline', location = 'right')
    bar_style = xml.SubElement(barline, 'bar-style').text = 'light-heavy'
    file.close()

    tree = xml.ElementTree(score_partwise)
    with open(fileName,'wb') as files:
        tree.write(files)

def get_audio_paths(audio_dir):  #Para conseguir la dirección completa del archivo mp3 con el nombre
    return [os.path.join(root, fname) for (root, dir_names, file_names) in os.walk(audio_dir, followlinks=True)
            for fname in file_names if (fname.lower().endswith('.wav') or fname.lower().endswith('.mp3'))]

def song_name(ruta):
    audio = str(get_audio_paths(ruta))
    audio = audio.split('\\')
    cancion = audio[-1].split('.')
    return cancion[0]

def main (): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_dir", type=str)
    parser.add_argument('--bpm', type=int,default=90)
    parser.add_argument('--minChordDuration', type=float,default=0.6)
    args = parser.parse_args() 
    subprocess.call(["python", "./test.py",'--audio_dir',args.audio_dir])
    nombre = song_name(args.audio_dir)
    initial_file_reading(args.bpm, args.minChordDuration, nombre)
    file_processing()
    bucles = list(repetitions(detection_loop_strings()))
    #bucles = loop_election()
    for i in bucles:
        print(i[0])
        loop_delete(i[0])
    generate_XML('./Proyecto/JjazzTab/'+nombre+'.xml',args.bpm,nombre)

if __name__ == '__main__':
    main()