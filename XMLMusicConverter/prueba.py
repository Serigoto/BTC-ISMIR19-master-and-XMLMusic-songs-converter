import re
import math
import xml.etree.cElementTree as xml

def repetitions(s):
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))

def lecturaInicialFichero(): #Lectura del fichero eliminando los acordes basura y añadiendo la variable de erealpro 
    file = open('./Proyecto/Acordes/example.lab', 'r')
    fileResult = open('./Proyecto/sinBucles/exampleTransitionRepeticiones.lab', 'w')
    lines = file.readlines()
    duracionMinima = 0.6
    bpm = 72
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
            line = str(aux[0]) + ' ' + str(aux[1]) + ' ' +letra +' '+ str(duracion) + ' ' +str(erealproT)
            fileResult.write(line+'\n')
    file.close()
    fileResult.close()
    
def deteccionCadenaBucles(): #Detecta los bucles en la canción
    file = open('./Proyecto/sinBucles/exampleCompletoRepeticiones.lab', 'r')
    lines = file.readlines()
    cadena = ''
    for index, line in enumerate(lines):
        aux = line.split()
        cadena += aux[2]
    file.close()
    return cadena

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
    num= 1
    file = open('./Proyecto/sinBucles/exampleCompletoRepeticiones.lab', 'r')
    lines = file.readlines()
    for index121, line1 in enumerate(lines):
        aux = line1.split()
        print(aux[2])
        tonalidad = 'major'
        if ':min' in aux[2]:
            tonalidad = 'minor'
            aux[2] = aux[2].replace(':min','')
        if duracion >= 3072:
            duracion = duracion - 3072 + int (aux[4])
            num += 1
            measure =xml.SubElement(part,'measure',number = str(num))
            harmony = xml.SubElement(measure, 'harmony',print_frame = 'no', default_y = '25',relative_x = '10')
            root = xml.SubElement(harmony, 'root')
            root_step = xml.SubElement(root, 'root-step').text = aux[2]
            root_alter = xml.SubElement(root, 'root-alter').text = '0'
            kind = xml.SubElement(harmony, 'kind').text = tonalidad
            note = xml.SubElement(measure, 'note')
            pitch = xml.SubElement(note, 'pitch')
            step = xml.SubElement(pitch, 'step').text = 'B'
            octave = xml.SubElement(pitch, 'pitch').text = '4'
            if duracion > 3072:
                duracion = duracion
                duration = xml.SubElement(note, 'duration').text = str(duracion)
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
                duracion = duracion + int(aux[4]) - 3072
                num +=1
                measure =xml.SubElement(part,'measure',number = str(num))
                harmony = xml.SubElement(measure, 'harmony',print_frame = 'no', default_y = '25',relative_x = '10')
                root = xml.SubElement(harmony, 'root')
                root_step = xml.SubElement(root, 'root-step').text = aux[2]
                root_alter = xml.SubElement(root, 'root-alter').text = '0'
                kind = xml.SubElement(harmony, 'kind').text = tonalidad
                note = xml.SubElement(measure, 'note')
                pitch = xml.SubElement(note, 'pitch')
                step = xml.SubElement(pitch, 'step').text = 'B'
                octave = xml.SubElement(pitch, 'pitch').text = '4'
                duration = xml.SubElement(note, 'duration').text = aux[4]
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
            else: 
                duration = xml.SubElement(note, 'duration').text = aux[4]
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
        else:
            harmony = xml.SubElement(measure, 'harmony',print_frame = 'no', default_y = '25',relative_x = '10')
            root = xml.SubElement(harmony, 'root')
            root_step = xml.SubElement(root, 'root-step').text = aux[2]
            root_alter = xml.SubElement(root, 'root-alter').text = '0'
            kind = xml.SubElement(harmony, 'kind').text = tonalidad
            note = xml.SubElement(measure, 'note')
            pitch = xml.SubElement(note, 'pitch')
            step = xml.SubElement(pitch, 'step').text = 'B'
            octave = xml.SubElement(pitch, 'pitch').text = '4'
            if duracion +int(aux[4]) > 3072:
                resto = 3072 -duracion
                duration = xml.SubElement(note, 'duration').text = str(resto)
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
                duracion = int(aux[4]) - resto
                num +=1
                measure =xml.SubElement(part,'measure',number = str(num))
                harmony = xml.SubElement(measure, 'harmony',print_frame = 'no', default_y = '25',relative_x = '10')
                root = xml.SubElement(harmony, 'root')
                root_step = xml.SubElement(root, 'root-step').text = aux[2]
                root_alter = xml.SubElement(root, 'root-alter').text = '0'
                kind = xml.SubElement(harmony, 'kind').text = tonalidad
                note = xml.SubElement(measure, 'note')
                pitch = xml.SubElement(note, 'pitch')
                step = xml.SubElement(pitch, 'step').text = 'B'
                octave = xml.SubElement(pitch, 'pitch').text = '4'
                duration = xml.SubElement(note, 'duration').text = str(duracion)
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
            else: 
                duration = xml.SubElement(note, 'duration').text = aux[4]
                notehead = xml.SubElement(note, 'notehead').text = 'diamond'
                duracion +=int(aux[4])
    barline = xml.SubElement(measure, 'barline', location = 'right')
    bar_style = xml.SubElement(barline, 'bar-style').text = 'light-heavy'
    file.close()

    tree = xml.ElementTree(score_partwise)
    with open(fileName,'wb') as files:
        tree.write(files)
    
def eliminarBucles(cadena):
    file = open('./Proyecto/sinBucles/exampleCompletoRepeticiones.lab', 'r')
    fileResult = open('./Proyecto/sinBucles/exampleAuxiliar.lab','w')
    lines = file.readlines()
    cont = 0
    cont2 = 0
    buffer = []
    for index, line in enumerate(lines):
        aux = line.split()
        chord = aux[2].replace(':min','')
        if cont != len(cadena):
            cont2 = 0
            buffer = []
            if cadena[cont] == chord:
                cont += 1
            else:
                cont = 0
            fileResult.write(line)
        else:
            if cont2 != len(cadena):
                if cadena[cont2] == chord:
                    cont2 += 1
                    buffer.append(line)
                else:
                    cont2 = 0
                    for i in buffer:       
                        fileResult.write(i)
                    fileResult.write(line)
                    cont = 0
                    if cadena[cont] == chord:
                        cont += 1
            else:
                cont2 = 0
                buffer = []
                if cadena[cont2] == chord:
                    cont2 = 1
                    buffer.append(line)
                else:
                    fileResult.write(line)
    fileResult.close()
    file.close()

    file = open('./Proyecto/sinBucles/exampleAuxiliar.lab', 'r')
    fileResult = open('./Proyecto/sinBucles/exampleCompletoRepeticiones.lab','w')
    lines = file.readlines()
    for index, line in enumerate(lines):
        fileResult.write(line)
    fileResult.close()
    file.close()

def tratamientoFichero():   #Quita los acordes iguales que están seguidos y suma las duraciones
    file = open('./Proyecto/sinBucles/exampleTransitionRepeticiones.lab', 'r')
    fileResult = open('./Proyecto/sinBucles/exampleCompletoRepeticiones.lab','w')
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

def eleccionBucles():
    chordList=(list(repetitions(deteccionCadenaBucles())))
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

def comparar():
    file = open('./Proyecto/sinBucles/exampleCompletoRepeticiones.lab', 'r')
    lines = file.readlines()
    cadena = ''
    for index, line in enumerate(lines):
        chord = line.split()
        #print(chord[2])
    file.close()

def main():
    lecturaInicialFichero()
    tratamientoFichero()
    bucles = eleccionBucles()
    for i in bucles:
        eliminarBucles(i)
    comparar()
    generateXML('./Proyecto/JjazzTab/exampleSinBucles.xml')

if __name__ == '__main__':
    main()