import json
from utils.special_massive import tids_items

def get_message_by(mid, data=None):
    '''
    :param mid -> str, int: message ID for return
    :param data -> str, int, list: дополнительные данные
    :return: message

    Позволяет выводить сообщение по ключевым ID.

    Для просмотр доступных, зайдите в файл utils/texts.py
    '''
    if mid == 'welcome':
        text = '''Добро пожалователь в <b>постапокалипстический игровой мир.</b>
Здесь Вы можете сражаться, добывать ресурсы, отстраивать базы, искать пропитание, возводить отряды или кланы и многое другое...
Игровой мир построен на базе визуализационной текстовой игры - где все Ваши действия, это нажатия на специальные кнопки или ввод команд для воспроизведения действия от имени персонажа.

Для того, чтобы узнать лор и сюжет игры, нажмите <b><i>"Лор"</i></b>
После прочтения Лора можно будет зарегистрироваться.

Для того, чтобы узнать действующие игровые механики, нажмите <b><i>"Игровые механики"</i></b>

<b>Приятного времяпрепровождения!</b>
        '''
    elif mid == 'main':
        if data is not None:
            text = f'''@{data[2]}, Вы на главной.

Выберите необходимое действие:
'''
    elif mid == 'lore_0':
        text = '''<i>Уже конец 2039 года. Время года - Зима.</i> Процветающий 21 век своими передовыми информационными технологиями сражался в гонке вооружений. 
Каждый политик пытался выхватить в "гонке" что-то свое, либо наоборот выйти из неё. Никто не думал, что среди всех передовых технологий, начнут применять биологическое оружие на возрастающей цивилизации.
<b><i>Действия разворачиваются в некой стране N.</i></b>

<b><i>12 ноября 2039 года. Записи одного ученого.</i></b>
-> 
Я, Вариц Алекс, конспектирую третий год подряд. Испытание специальной инъекции "Виарум" прошло успешно на подопытных в виде мышей и остальных грызунов. 
Подопытные мутировали и утратили свое мышление, сознание, оставляя позади животные повадки. У них появилось лишь одно - убивать и поедать. 
Инстинкты подопытных возрасли многократно, из-за чего те начали беспрепятственно пытаться напасть на моих коллег.

Правительство требует выпустить иъекцию.. нет, правильнее сказать, вирус, биооружие в массовое производство. Для каких целей непонятно...

Веду исследование дальше...

<b><i>2 декабря 2039 года. Записи одного ученого.</i></b>
->  
- Алекс, у нас выходит все из-под контроля! Грызуны начали сбегать! Что делать?
- Мы ей ничем больше не поможем, убивай её...

Прошу прощения. Специальная инъекция "Виарум" начала передаваться военизированным службам в целях успокоения и напугивания иностранных сил, выступающих против страны.
Неизвестно, как правительство будет применять вирус, и как именно он может перепасть из одних рук в другие. Ясно одно, это к хорошему не приведет.

- Алекс, военные уже здесь! Прячь биологичку!
<b>* ПОМЕХИ-ПОМЕХИ-ПОМЕХИ *</b>

<b><i>2 февраля 2040 года. Записи военного. *ЗАСЕКРЕЧЕНО*</i></b>
->  - Правителство начинает контрмеры против враждующих стран. Биологическое оружие было заряжено в боеголовки и зарегистрированы как испытательные ракеты невредоносного происхождения.
Предотвратить не является возможным. Все военные были выведены из боевых действий и отосланы в отставку связи с переполнением казарм. Мало верится, но что же будет дальше?

<b>Никому. Не. Известно.</b>

<b>* ПОМЕХИ-ПОМЕХИ-ПОМЕХИ*</b>
        '''
    elif mid == 'lore_1':
        text = '''Правительство начало крупную военную операцию, как казалось, с применением оружия массового поражения и биологического содержания. 
Связи с этим, в мировом конгрессе объявлено чрезвычайное положение. Объявлен карантин. Людям запретили выходить на улицы, дабы не попасть под удар биооружия.

Все так думали, что все кончится хорошо.

<b><i>7 апреля 2040 года.</i></b>
Правительство страны N запустило первые испытательные ракеты биологического происхождения. Результаты оказались на их стороне. Множество вражеских сил было повержено и превращены в монстров, которые разлагаются на месте.
Политики "в восторге" от происходящего. Военные пытаются остановить правительство, но безуспешно. Половина военных встала на сторону правительства, остальная половина образовало военизированную организацию повстанцев "Аббелиск" (ВОП "Аббелиск")

Предназначение ВОП "Аббелиск" остановить правительство в масштабной войне и прекратить выпуск биологического оружия "Виарум-1", предвращая ненужные жертвы.

<b><i>12 июня 2040 года.</i></b>
У "Аббелиск" - ничего не получилось. Правительство оказало существенное сопротивление повстанцам, не щадя их, а просто зверски убивая, посылая и на них мельчайшие частицы биооружия уже в виде обычных пуль.

<b><i>20 июня 2040 года.</i></b>
Правительство запускает ракеты массового поражения по соседним странам. Началась крупномасштабная война в стране N и её приближенных государств.

<b><i>1 июля 2040 года.</i></b>
Катастрофа. Страна N и приближенные к ней другие государства обратились в руины, в полчища мутантов и потерявших способность мыслить людей.

Правительство потерпело крах, люди стали невыносимо страдать, половина зданий превратились в дома для мутантов, и только малая часть сохранилась в прежнем виде, но и туда уже добрались мародеры.

"Аббелиск", как бывший отряд военных, вновь нашелся. Бывшие участники собрались вместе, вновь образуя коалицию по возвращению цивилизации в прежний вид.
"Аббелиск" занял окрайну города, отстроив свою базу. 

Бывшие члены правительственного комитета и военные воссоздали небольшую организацию, занимающуюся сбором людей и возвращением контроля над ситуацией.

Есть и бандитские организации, которые занимаются мародерством - "Мавеот" и "Нивелим".
Каждая из организаций имеет своих лидеров и свои устои, что предстоит еще раскрыть.

"Аббелиск", как бывшая ВОП, восстала против бывших членов правительственного комитета, и собирает людей, дабы образумить бывшее правительство и восстановить ситуацию такой, какая она была до войны.

На встречу всем, выходят мутанты, ныне называемые, как зомби и их различные подвиды. 

Так ли должна была закончиться война или у правительства были еще мотивы? Кто за этим стоит? Множество тайн осталось не раскрыто...

Следите за своим здоровьем, ищите ресурсы, создавайте предметы и убивайте мутантов и неблагодарных мародеров, искореняющих даже мирных оставшихся в живых людей.
Создайте свой клан или отряд, либо присоединитесь к глобальным организациям, например, к "Аббелиску".

<b>Боритесь за свою жизнь.</b>
'''
    elif mid == 'game_mechanics':
        text = '''<b>Основные механики игры:</b>
🌍 <b>Игровой мир</b>
⚔️ <b>PvP и PvE режимы</b>
🛡️ <b>Клановая система</b> 
🧟 <b>Боссы</b>
👑 <b>Рейтинговая система</b>
📜 <b>Система квестов</b>

📌❓ Чтобы узнать о каждой механике подробнее, выберите необходимую механику ниже:
        '''
    elif mid == 'game_mechanic_game_world':
        text = '''🌍 <b>Игровой мир</b>
В данную механику входят следующие элементы:
1. Исследование локаций, зданий.
2. Поиск ресурсов
3. Сражение с мутантами и игроками.
        '''
    elif mid == 'game_mechanic_pv-pe_mode':
        text = '''⚔️ <b>PvP и PvE режимы</b>
Основная игровая механика, предполагающая собой как механику PvP (против игроков и мутантов) с исследованием территорий, но также PvE (только против мутантов).
В режиме PvE частота выпадение редких вещей и особых наград ниже.
Квесты в PvE имеют особый приоритет, при помощи режима PvE можно будет спокойно проходить сюжетную линию игры, несмотря на игроков.
В PvP сложность повышается. Боссы, ресурсы появляются с более большой частотой, но и игроки, прошедшие через многое, могут с легкостью Вас убить.
Имейте ввиду, что в PvP есть возможность собраться отрядом и пойти против игроков с мутантами.
PvE предполагает совместное прохождение определенных квестов (за исключением сюжетных).
        '''
    elif mid == 'game_mechanic_clan_system':
        text = '''🛡️ <b>Клановая система</b> 
В данную механику входят следующие элементы:
1. Клановое сообщество и статистика клана.
2. Клановые войны.
3. Масштабное исследование локаций (предполагает сбор участников в поход)
4. Групповое убийство мутантов.
        '''
    elif mid == 'game_mechanic_zombie_bosses':
        text = '''🧟 <b>Боссы</b>
Данная механика нацелена на групповое/одиночное противостояние против мощных мутантов или их полчищ в виде босса.
Как и сказано выше, можно будет напасть в одиночку (но с низким шансом победы), так и отрядом/кланом.
        '''
    elif mid == 'game_mechanic_rating_system':
        text = '''👑 <b>Рейтинговая система</b>
Механика включает в себя противостояние между кланами за лидерством, либо игроками.
Рейтинг между кланами - очки кланов, зарабатываемые за совместное выполнение клановых заданий, убийств боссов.
Рейтинг между игроками - убийства и уровень.
        '''
    elif mid == 'game_mechanic_quests_system':
        text = '''📜 <b>Система квестов</b>
Механика предполагает выполнение сюжетных, побочных и клановых квестов.
В сюжетные квесты, как понятно, входит выполнение лора и следование по течению игры, а также выбор особенных путей.
Сюжетные квесты нельзя выполнять отрядом, только в одиночку.
Побочные квесты выдаются квестовиками (NPC), имеют различное происхождение (на основе рандома).
В побочные квесты также входят ежедневные подзадания, пример: убить 10 зомби-химер.
"Побочки" можно выполнить как в одиночку, так и отрядом.
Клановые квесты предполагают выполнение определенных условных действий всего клана.
Действия предполагают собой выполнение цепочки заданий за счет чего начисляются клановые "очки".
        '''
    elif mid == 'complete_reg':
        if data is not None:
            text = f'''{data}, ✅ Ваш аккаунт успешно зарегистрирован.

<b>Не переживайте, Вы еще можете выжить...</b>            

<b>Начать игру?</b>
'''
    elif mid == 'start_game_first':
        text = '''Состояние ужасное. В какой-то момент, Вы перестали ощущать свое тело в мгновение ока. 
Не понимаете, что произошло. Вокруг все потемнело, Вы упали без сознания. 

Что же могло произойти? Ядерная атака? Катастрофа. Ужасные события закрутились вокруг страны N.

<b>ВАМ НУЖНО ВЫЖИТЬ!</b>

Вы начали приходить в себя, в Ваших ушах остался пронзительный звон громких сирен. 
Потихоньку, этот пронзительный звон пропал и Вы начали слышать звуки воды...

Открыть глаза?
'''
    elif mid == 'inventory':
        if data is not None:
            text = data
        else:
            text = 'Ваш инвентарь пуст.'
    elif mid == 'item_info_inv':
        if data[4] != 'Нет':
            stats_json = json.loads(data[4])
            print(type(stats_json))
            if data[2] == 'Оружие':
                stats_item = f'''
⋙ Урон: {stats_json["damage"]}
⋙ Прочность: {stats_json["health"]}
⋙ Трата энергии: {stats_json["energy"]}
⋙ Скорость атаки: {stats_json["speed"]}
'''
        else:
            stats_item = 'Нет'
        if data is not None:
            text = f'''Предмет: {data[1]}
├ Тип: {data[2]}
├ Редкость: {data[3]}
├ Статистика: 
{stats_item}
└ Описание: {data[5]}

Можно ли продавать (NPC): {"Да" if data[6] == 1 else "Нет"}
Можно ли продавать (Аукцион): {"Да" if data[7] == 1 else "Нет"}
'''
    return text

def get_game_message_by(mid, data=None):
    '''
    :param mid -> str, int: id сообщения
    :param data -> str, int, list: дополнительные данные

    Позволяет возвращать текст сообщения по специальному ID.
    
    Для просмотра ID, перейдите в файл utils/texts.py
    '''
    if mid == 'prology_0':
        if data is not None:
            text = f'''Открывая свои глаза, Вы видите на себе порванные тряпки, а рядом с Вами лежит ржавый нож.
Вы неспешно поднимаете нож, не понимая, что здесь происходит. 

Вы оглядываетесь по сторонам. Наблюдаете следующее...
{data[2]}

Что же делать? Нужно найти <b>выжившего</b>, у кого можно спросить...
    '''
    return text