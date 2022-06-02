import math
from email import message
from email.policy import default
from pyexpat.errors import XML_ERROR_UNKNOWN_ENCODING
from statistics import harmonic_mean
import xml.etree.cElementTree as xml
import argparse
import subprocess

def lecturaFichero(): #Lee el fichero que genera el BTC y añade la variable de erealpro
                        #Elimina los acordes residuales
    file = open('./Proyecto/Acordes/example.lab', 'r') #Ubicacion del .tab creado por el BTC
    fileResult = open('./Proyecto/Transicion/exampleTransition.lab', 'w') # Fichero donde se van a escribir los datos tratados
    lines = file.readlines()
    bpm = int(input('BPM de la canción: '))
    #bpm = 71
    #spm1 = 60/bpm
    spm2 = 60/bpm*2
    #spm3 = 60/bpm*3
    spm4 = 60/bpm*4
    # spm5 = 60/bpm*4 + 60/bpm
    # spm6 = 60/bpm*4 + 2*60/bpm
    # spm7 = 60/bpm*4 + 3*60/bpm
    # spm8 = 60/bpm*4 + 4*60/bpm
    #print (spm1, spm2, spm3, spm4, spm5, spm6, spm7, spm8)
    erealpro = 3072
    desviacion = 0.5
    for index, line in enumerate(lines):
        aux = line.split()
        duracion = round(float(aux[1]) - float(aux[0]),3)
        letra = aux[2]
        if duracion > 0.6:
            if math.isclose(spm2,duracion, abs_tol=desviacion):
                erealpro = 1536
            elif math.isclose(spm4,duracion, abs_tol=desviacion):
                erealpro = 3072
            line = str(aux[0]) + ' ' + str(aux[1]) + ' ' +letra +' '+ str(duracion) + ' ' +str(erealpro)
            fileResult.write(line+'\n')
    file.close()
    fileResult.close()

def tratamientoFichero():   #Quita los acordes iguales que están seguidos y suma las duraciones
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
                    line = str(prechord[0]) + ' ' + str(prechord[1]) + ' ' +prechord[2] +' '+ str(mod) + ' ' +prechord[4]
                else : 
                    line = str(prechord[0]) + ' ' + str(prechord[1]) + ' ' +prechord[2] +' '+ prechord[3] + ' ' +prechord[4]
                prechord = chord
                fileResult.write(line+'\n')
        else :
            prechord = chord
    line = str(chord[0]) + ' ' + chord[1] + ' ' +chord[2] +' '+ chord[3] + ' ' +chord[4]
    fileResult.write(line+'\n')
    fileResult.close()
    file.close()

def generateXML(fileName):  #Lee el fichero de acordes tratado y crea el XML
    score_partwise = xml.Element("score-partwise",version="2.0")
    movement_title = xml.SubElement(score_partwise,'movement-title').text = 'Hurt (Cash)'
    identification = xml.SubElement(score_partwise,'identification')
    creator = xml.SubElement(identification,'creator',type = 'composer  ').text =  'Reznor'
    creator = xml.SubElement(identification,'creator',type = 'lyricst').text =  '91bpm'
    rights = xml.SubElement(identification,'rights').text =  'Made with iReal Pro'
    encoding = xml.SubElement(identification,'encoding')
    software = xml.SubElement(encoding,'software').text = 'iReal Pro (Android)'
    encoding_date = xml.SubElement(encoding,'encoding-date').text = '2022-05-06'
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
    
    system_layout = xml.SubElement(defaults,'system-layout')
    system_margins = xml.SubElement(system_layout,'system-margins')
    left_margin = xml.SubElement(system_margins,'left-margin').text = '22'
    right_margin = xml.SubElement(system_margins,'right-margin').text = '0'
    system_distance = xml.SubElement(system_layout,'system-distance').text = '100'
    top_system_distance = xml.SubElement(system_layout,'top-system-distance').text = '73'
    appearance = xml.SubElement(defaults, 'appearance', type = 'beam')
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
    music_font = xml.SubElement(defaults, 'music_font',font_family = 'Opus,music')
    word_font = xml.SubElement(defaults, 'word-font', font_family= 'Time New Roman')
    part_list = xml.SubElement(score_partwise, 'part-list')
    score_part = xml.SubElement(part_list, 'part',id = 'P1')
    part_name = xml.SubElement(score_part, 'part-name', print_object = 'no').text = 'Lead sheet'
    
    part = xml.SubElement(score_partwise, 'part', id = 'P1')
    measure = xml.SubElement(part, 'measure',number = '1')
    print_1 = xml.SubElement(measure, 'print')
    system_layout = xml.SubElement(print_1, 'system-layout')
    top_system_distance = xml.SubElement(system_layout, 'top-system-distance').text = '210'

    attributes = xml.SubElement(measure,'atributes')
    divisions = xml.SubElement(attributes,'divisions').text ='768'
    key = xml.SubElement(attributes, 'key')
    fifhts = xml.SubElement(key,'fifths').text = '0'
    mode = xml.SubElement(key, 'mode').text = 'minor'
    time = xml.SubElement(attributes, 'time')
    beats = xml.SubElement(time, 'beats').text = '4'
    beat_type = xml.SubElement(time, 'beat-type').text = '4'
    clef = xml.SubElement(attributes,'clef')
    sign = xml.SubElement(clef, 'sign').text = 'G'
    line = xml.SubElement(clef, 'line').text = '2'
    direction = xml.SubElement(measure, 'direction', placement = 'above')
    direction_type = xml.SubElement(direction, 'direction-type')
    words = xml.SubElement(direction_type,'words').text = 'Tutti, Inst'
    barLine = xml.SubElement(measure, 'barLine', location = 'right')
    bar_style = xml.SubElement(barLine, 'bar-style').text = 'light-light'
    direction2 = xml.SubElement(measure, 'direction', placement = 'above')
    direction_type2 = xml.SubElement(direction2, 'direction-type')
    rehearsal = xml.SubElement(direction_type2, 'rehearsal').text = 'intro'
    measure =xml.SubElement(part,'measure',number = '1')

    #LECTURA DEL FICHERO PARA COMPLETAR EL XML
    duracion = 0
    file = open('./Proyecto/Transicion/exampleCompleto.lab', 'r')
    lines = file.readlines()
    for index121, line1 in enumerate(lines):
        aux = line1.split()
        tonalidad = 'major'
        if ':min' in aux[2]:
            tonalidad = 'minor'
        if duracion >= 3072:
            duracion = 0
            numero = 1 + index121
            measure =xml.SubElement(part,'measure',number = str(numero))
        if duracion <= 3072:
            harmony = xml.SubElement(measure, 'harmony',print_frame = 'no', default_y = '25',relative_x = '10')
            root = xml.SubElement(harmony, 'root')
            root_step = xml.SubElement(root, 'root-step').text = aux[2][0]
            root_alter = xml.SubElement(root, 'root-alter').text = '0'
            kind = xml.SubElement(harmony, 'kind').text = tonalidad
            note = xml.SubElement(measure, 'note')
            pitch = xml.SubElement(note, 'pitch')
            step = xml.SubElement(pitch, 'step').text = 'B'
            octave = xml.SubElement(pitch, 'pitch').text = '4'
            duration = xml.SubElement(note, 'duration').text = aux[4]
            #type1 = xml.SubElement(note, 'type').text = 'whole'
            notehead = xml.SubElement(note, 'notehead').text = 'diamond'
            duracion = duracion + int(aux[4])
            if duracion > 3072:
                numero = 1 + index121
                measure =xml.SubElement(part,'measure',number = str(numero))
                duracion = duracion - 3072
                harmony = xml.SubElement(measure, 'harmony',print_frame = 'no', default_y = '25',relative_x = '10')
                root = xml.SubElement(harmony, 'root')
                root_step = xml.SubElement(root, 'root-step').text = aux[2][0]
                root_alter = xml.SubElement(root, 'root-alter').text = '0'
                kind = xml.SubElement(harmony, 'kind').text = tonalidad
                note = xml.SubElement(measure, 'note')
                pitch = xml.SubElement(note, 'pitch')
                step = xml.SubElement(pitch, 'step').text = 'B'
                octave = xml.SubElement(pitch, 'pitch').text = '4'
                duration = xml.SubElement(note, 'duration').text = aux[4]
                #type1 = xml.SubElement(note, 'type').text = 'whole'
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
                
    barline = xml.SubElement(measure, 'barline', location = 'right')
    bar_style = xml.SubElement(barline, 'bar-style').text = 'light-heavy'
    file.close()

    tree = xml.ElementTree(score_partwise)
    with open(fileName,'wb') as files:
        tree.write(files)
def main (): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_dir", "-a")
    args = parser.parse_args() # TENGO LA DIRECCION DONDE ESTÁ EL ARCHIVO MP3
    subprocess.call(["python", "./test.py",'--audio_dir',args.audio_dir])   #LLAMADA A test.py  CON EL LA RUTA ANTERIOR PARA QUE GENERE EL .tab
    lecturaFichero()
    tratamientoFichero()
    generateXML('./Proyecto/JjazzTab/example.xml')

if __name__ == '__main__':
    main()