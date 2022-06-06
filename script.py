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
from torch import long

def overlap_removal(valido):
    inicios = valido[0]
    repeticiones = valido[1]
    longitud = valido[2]

    inicios = [int(x) for x in inicios]
    repeticiones = [int(x) for x in repeticiones]
    longitud = int(longitud)

    for i in range(0, len(inicios)):
        limite = inicios[i]+longitud*repeticiones[i]
        rango = range(inicios[i]+1,limite)
        for j in rango:
            if j in inicios:
                posicion = inicios.index(j)
                inicios[posicion] = -1
                repeticiones[posicion] = 0

    inicios = [i for i in inicios if i != -1]
    repeticiones = [i for i in repeticiones if i != 0]
    return inicios, repeticiones, longitud

def repetitions(s): #Detecta repeticiones en la canción ya tratada
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))

def initial_file_reading(argBPM, minChordDuration, nombre): #Lee el fichero que genera el BTC y añade la variable de irealpro
                                            #Elimina los acordes residuales y añade variable del loops
    file = open('./XMLMusicConverter/Acordes/'+nombre+'.lab', 'r')
    fileResult = open('./XMLMusicConverter/Transicion/exampleTransition.lab', 'w')
    lines = file.readlines()
    duracionMinima = minChordDuration
    bpm = argBPM
    spm = 60/bpm
    spmT = spm
    irealpro = 768
    irealproT = irealpro
    desviacion = spm/2

    for index, line in enumerate(lines):
        aux = line.split()
        duracion = round(float(aux[1]) - float(aux[0]),3)
        letra = aux[2]
        if letra != 'N':
            if duracion > duracionMinima:
                spmT = spm
                irealproT = irealpro
                while not math.isclose(spmT, duracion, abs_tol=desviacion):
                    spmT +=spm
                    irealproT += irealpro
                line = str(aux[0]) + ' ' + str(aux[1]) + ' ' +letra +' '+ str(duracion) + ' ' +str(irealproT) + ' ' + str(0)+ ' ' + str(0)
                fileResult.write(line+'\n')
    file.close()
    fileResult.close()

def get_string_chords(): #lee la cadena de toda la cancion
    file = open('./XMLMusicConverter/Transicion/labtipoxml.lab', 'r')
    lines = file.readlines()
    cadena = ''
    for index, line in enumerate(lines):
        aux = line.split()
        cadena = cadena +aux[2]+ ','
    file.close()
    return cadena

def loop_removal (resul):
    inicios = resul[0]
    repeticiones = resul[1]
    longitud = resul[2]
    print(resul)
    cont = 0
    flag = False
    file = open('./XMLMusicConverter/Transicion/labtipoxml.lab', 'r')
    lines = file.readlines()
    i = 0
    if inicios:
        fileResult = open('./XMLMusicConverter/Transicion/labtipoxml.lab', 'w')
        flag = False
        cont = 0
        for index, line in enumerate(lines):
            aux = line.split()
            if int(inicios[i]) == index and aux[5] == '0':
                cont = 0
                flag = True
                datos = aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+aux[4]+' '+str(repeticiones[i])+' '+str(longitud)
                fileResult.write(datos+'\n')
            else:
                if flag:
                    if cont < longitud-1:
                        cont += 1
                        datos = aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+aux[4]+' '+str(repeticiones[i])+' '+str(longitud)
                        fileResult.write(datos+'\n')
                    else:
                        if cont >= longitud-1 and cont < (longitud*repeticiones[i])-1:
                            cont += 1
                        else:
                            fileResult.write(line)
                            flag = False
                            cont = 0
                            i += 1
                            if i == len(repeticiones):
                                i = 0
                else:
                    fileResult.write(line)
        file.close()
        fileResult.close()
    
    file = open('./XMLMusicConverter/Transicion/labtipoxml.lab', 'r')

def real_loop_detector (resul):
    cadena = resul[0]
    inicios = resul[1]
    longitud = resul[2]
    repeticiones = []
    lista = []
    contador = 1
    suma = 0
    for i in inicios:
        suma = int(i)+ int(longitud)
        while suma in inicios:
            contador += 1
            suma += int(longitud)
        if contador > 1:
            repeticiones.append(contador)
            lista.append(i)
        contador = 1
        suma = 0
    return lista, repeticiones, longitud

def loop_election(): 
    loopList=(list(repetitions(get_string_chords())))
    elegidos = []
    for i in loopList:
        if len(i[0]) > 2:   #Eliminalos loops con solo un acorde
            resul = loop_validation(i[0]) #Loops exactos (empiezan con el compás vacío y terminan completando el compás)
            if resul[1]:    #Si existe esa cadena de forma 'exacta'
                valido = real_loop_detector(resul) #Comprueba si esa cadena se encuentra seguida por lo menos 2 veces
                if valido[0]: #Si ha encontrado alguna cadena seguida almenos una vez    valido = lista, repeticiones, longitud
                    loop_removal(overlap_removal(valido)) #Elimina el bucle

def loop_validation(cadena):
    aux = cadena.replace(':min','')
    aux = aux.replace(',','')
    aux = aux.replace('#','')
    longitud = len(aux)

    irealpro = 0        #Desde 0 a 3072
    if cadena[0] == ',':
        cadena = cadena[1:]
    else:
        cadena = cadena[:-1]
    cadena = cadena.split(',')
    contCadena = 0
    flag = False
    inicios = []
    first = 0
    file = open('./XMLMusicConverter/Transicion/labtipoxml.lab', 'r')
    lines = file.readlines()
    if len(cadena) >1:
        for index, line in enumerate(lines):
            aux = line.split()
            chord = aux[2]
            if irealpro == 0 and cadena[contCadena] == chord and flag == False:
                contCadena += 1
                first = index
                flag = True
            else:
                if flag:
                    if cadena[contCadena] == chord:
                        contCadena += 1
                    else:
                        contCadena = 0
                        flag = False
                    if contCadena == longitud:
                        if irealpro+int(aux[4])== 3072:
                            inicios.append(first)
                        flag = False
                        contCadena = 0
            irealpro += int(aux[4])
            if irealpro >= 3072:
                irealpro -= 3072
    return cadena, inicios,longitud

def file_processing():   #Quita los acordes iguales que están seguidos y suma las duraciones
    file = open('./XMLMusicConverter/Transicion/exampleTransition.lab', 'r')
    fileResult = open('./XMLMusicConverter/Transicion/exampleCompleto.lab','w')
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
    contMeasure = 1
    flag = False
    file = open('./XMLMusicConverter/Transicion/labtipoxml.lab', 'r')
    lines = file.readlines()
    cont = 0
    nota = ''
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
        if aux[4] == '3072':
            nota = 'whole'
        elif aux[4] == '1536':
            nota = 'half'
        elif aux[4] == '768':
            nota = 'quarter'

        if aux[2] != 'N':
            if duracion < 3072:
                duracion += int(aux[4])
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
                if aux[4] == '2304':
                    type2 = xml.SubElement(note, 'type').text = 'half'
                    dot = xml.SubElement(note,'dot')
                else:
                    type2 = xml.SubElement(note, 'type').text = nota
            else:
                contMeasure += 1
                duracion -=3072
                duracion += int(aux[4])
                measure =xml.SubElement(part,'measure',number = str(contMeasure))
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
                if aux[4] == '2304':
                    type2 = xml.SubElement(note, 'type').text = 'half'
                    dot = xml.SubElement(note,'dot')
                else:
                    type2 = xml.SubElement(note, 'type').text = nota
                

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

def xml_type_generator():
    file = open('./XMLMusicConverter/Transicion/exampleCompleto.lab', 'r')
    fileResult = open('./XMLMusicConverter/Transicion/labtipoxml.lab','w')
    lines = file.readlines()
    irealpro = 0
    resto = 0
    for index, line in enumerate(lines):
        aux = line.split()
        irealpro += int(aux[4])
        if irealpro > 3072:
            irealpro -= int(aux[4])
            resto = 3072 - irealpro
            fileResult.write(aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+str(resto)+' '+aux[5]+' '+aux[6]+' '+'\n')
            irealpro = int(aux[4]) - resto
            while irealpro > 3072:
                irealpro -= 3072
                fileResult.write(aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+'3072'+' '+aux[5]+' '+aux[6]+' '+'\n')
            if irealpro != 0:
                fileResult.write(aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+str(irealpro)+' '+aux[5]+' '+aux[6]+' '+'\n')
            if irealpro == 3072:
                irealpro = 0
        elif irealpro == 3072:
            irealpro = 0
            fileResult.write(aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+aux[4]+' '+aux[5]+' '+aux[6]+' '+'\n')
        else:
            fileResult.write(aux[0]+' '+aux[1]+' '+aux[2]+' '+aux[3]+' '+aux[4]+' '+aux[5]+' '+aux[6]+' '+'\n')
    file.close()
    fileResult.close()

def main (): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_dir", type=str,default='./test')
    parser.add_argument('--bpm', type=int,default=90)
    parser.add_argument('--min_chord_duration', type=float,default=0.6)
    args = parser.parse_args() 
    subprocess.call(["python", "./test.py",'--audio_dir',args.audio_dir])
    nombre = song_name(args.audio_dir)
    initial_file_reading(args.bpm, args.min_chord_duration, nombre)
    file_processing()
    xml_type_generator()
    loop_election()
    generate_XML('./XMLMusicConverter/MuseScore/'+nombre+'.xml',args.bpm,nombre)

if __name__ == '__main__':
    main()
