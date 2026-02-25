import time
import random

# ANSI colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
BOLD = "\033[1m"

SWORD = r"""
       />
 (======{>>>>>>>>>
       \\
"""

SKULL = r"""
      .-.
     (o.o)
      |=|
     __|__
   //.=|=.\\
  // .=|=. \\
  \\ .=|=. //
   \\(_=_)//
    (:| |:)
     || ||
     () ()
     || ||
     || ||
    ==' '==
"""

def warna(text, color_code):
    return f"{color_code}{text}{RESET}"

def cetak(text, color=None):
    if color:
        print(warna(text, color))
    else:
        print(text)
    time.sleep(0.5)

def roll(d=20):
    return random.randint(1, d)

def status(player):
    hp_bar = f"HP: {player['hp']}/{player['max_hp']}"
    xp_bar = f"XP: {player['xp']}/100"
    gold = f"Gold: {player.get('gold',0)}"
    cetak(warna(hp_bar + ' | ' + xp_bar + ' | ' + gold, CYAN))

def check_levelup(player):
    while player['xp'] >= 100:
        player['xp'] -= 100
        player['max_hp'] += 20
        player['hp'] = min(player['hp'] + 20, player['max_hp'])
        player['level'] += 1
        cetak(warna(f"LEVEL UP! Sekarang level {player['level']} — max HP +20.", GREEN))
        cetak(warna(SWORD, MAGENTA))

LOCATIONS = [
    ('Lembah Para Bijak', 'oasis teka-teki purba dan pengetahuan kuno'),
    ('Hutan Kabut', 'pepohonan berkabut yang menyimpan rahasia lama'),
    ('Kuil Runa', 'tempat rune kuno dan ritual bahasa arcanum'),
    ('Pelabuhan Patchhelm', 'tavern dan pasar pelaut, tempat tukang memperbaiki'),
    ('Puncak Bugbane', 'puncak legendaris yang menantang para pemberani')
]

def encounter(player, location):
    cetak(warna(f"Kamu menjelajahi {location[0]} — {location[1]}", BLUE))
    dice = roll(20)
    cetak(warna(f"Lempar dadu: {dice}", YELLOW))

    # flavor and outcomes
    if location[0] == 'Pelabuhan Patchhelm':
        cetak('Di pelabuhan ada pedagang, pelaut, dan seorang tua berkerudung yang tampak cemas.')
        cetak(warna('1) Beli potion (10 gold)  2) Bicara dengan pelaut  3) Dekati orang tua berkerudung', CYAN))
        pilihan = input(warna('Pilihan (1/2/3): ', CYAN)).strip()
        if pilihan == '1':
            if player.get('gold',0) >= 10:
                player['gold'] -= 10
                player.setdefault('potions',0)
                player['potions'] += 1
                cetak(warna('Kamu membeli potion. +1 potion.', GREEN))
            else:
                cetak(warna('Tidak cukup gold.', RED))
        elif pilihan == '2':
            cetak('Pelaut bercerita tentang sebuah Kuil Runa yang kehilangan fragmen rune.')
            cetak(warna('"Jika kau ambil fragmen itu, kuberikan 30 gold dan 30 XP" — tawarannya.', YELLOW))
            ambil = input(warna('Terima quest mengambil Fragmen Rune? (y/n): ', CYAN)).strip().lower()
            if ambil in ('y','yes'):
                q = {'id':'rune_frag', 'name':'Fragmen Rune', 'target':'Kuil Runa', 'reward_xp':30, 'reward_gold':30, 'completed':False}
                player.setdefault('quests', [])
                player['quests'].append(q)
                cetak(warna('Quest diterima: Ambil Fragmen Rune di Kuil Runa.', GREEN))
        elif pilihan == '3':
            cetak('Orang tua berkerudung memberimu peta kecil dan meminta bantuan mencari jimat ikan hilang di Hutan Kabut.')
            ambil = input(warna('Terima quest jimat ikan? (y/n): ', CYAN)).strip().lower()
            if ambil in ('y','yes'):
                q = {'id':'fish_amulet', 'name':'Jimat Ikan', 'target':'Hutan Kabut', 'reward_xp':20, 'reward_gold':15, 'completed':False}
                player.setdefault('quests', [])
                player['quests'].append(q)
                cetak(warna('Quest diterima: Temukan Jimat Ikan di Hutan Kabut.', GREEN))
        cetak('Kamu duduk di tavern, mendapatkan cerita dan sedikit pengalaman.')
        player['xp'] += 10
        return

    # encounter enemy difficulty varies by place
    difficulty = {
        'Lembah Para Bijak': 8,
        'Hutan Kabut': 10,
        'Kuil Runa': 12,
        'Puncak Bugbane': 15
    }
    target = difficulty.get(location[0], 10)

    if dice >= target:
        gain = random.choice([20,30,40])
        player['xp'] += gain
        gold_gain = random.randint(5,20)
        player['gold'] = player.get('gold',0) + gold_gain
        cetak(warna(f"Sukses! Kamu menang dalam encounter. +{gain} XP, +{gold_gain} gold.", GREEN))
        cetak(warna(SWORD, MAGENTA))
        # quest completion check on success
        for q in player.get('quests', []):
            if (not q.get('completed')) and q.get('target') == location[0]:
                q['completed'] = True
                player['xp'] += q.get('reward_xp',0)
                player['gold'] = player.get('gold',0) + q.get('reward_gold',0)
                cetak(warna(f"Quest selesai: {q['name']}! Hadiah: +{q.get('reward_xp',0)} XP, +{q.get('reward_gold',0)} gold.", YELLOW))
    else:
        # take damage based on location
        dmg = random.randint(10, 25)
        # class modifiers
        if player['cls'] == 'Warrior':
            dmg = max(5, dmg - 5)
        elif player['cls'] == 'Rogue' and dice > 5:
            dmg = max(3, dmg - 8)
        elif player['cls'] == 'Mage' and dice <= 5:
            dmg += 5

        player['hp'] -= dmg
        player['xp'] += 8
        cetak(warna(f"Gagal! Kamu terluka -{dmg} HP, tapi belajar banyak. +8 XP.", RED))
        if player['hp'] <= 0:
            cetak(warna('Kondisi kritis...', RED))
            cetak(warna(SKULL, RED))
        # even on failure, if location matches some quest, maybe find a clue (small reward)
        for q in player.get('quests', []):
            if (not q.get('completed')) and q.get('target') == location[0]:
                player['xp'] += 5
                cetak(warna(f"Walau gagal, kamu menemukan petunjuk kecil untuk quest {q['name']}. +5 XP.", YELLOW))

def choose_class():
    cetak('Pilih kelasmu (berikan nomor):')
    cetak(warna('1) Warrior — tahan banting (+20 HP start)', MAGENTA))
    cetak(warna('2) Rogue — serangan licik (chance kurangi damage)', YELLOW))
    cetak(warna('3) Mage — belajar cepat (+XP gain bonus)', BLUE))
    c = input(warna('Pilihan (1/2/3): ', CYAN)).strip()
    if c == '1':
        return 'Warrior'
    if c == '2':
        return 'Rogue'
    return 'Mage'

def rest_or_use(player):
    cetak('Apa yang ingin kamu lakukan?')
    cetak('1) Lanjut jelajah')
    cetak('2) Gunakan potion')
    cetak('3) Istirahat di tavern (pulih 30% HP, biaya 5 gold)')
    choice = input(warna('Pilih 1/2/3: ', CYAN)).strip()
    if choice == '2' and player.get('potions',0) > 0:
        player['potions'] -= 1
        heal = min(player['max_hp'] - player['hp'], 50)
        player['hp'] += heal
        cetak(warna(f'Kamu minum potion dan pulih {heal} HP.', GREEN))
    elif choice == '3' and player.get('gold',0) >= 5:
        player['gold'] -= 5
        heal = int(player['max_hp'] * 0.3)
        player['hp'] = min(player['max_hp'], player['hp'] + heal)
        cetak(warna(f'Istirahat: pulih {heal} HP.', GREEN))
    else:
        cetak('Lanjut petualangan...')

def game_loop(player):
    cetak(warna(f"Petualangan dimulai untuk {player['name']} si {player['cls']}.", BOLD+CYAN))
    while True:
        cetak('Daftar lokasi:')
        for i,loc in enumerate(LOCATIONS, start=1):
            cetak(warna(f"{i}) {loc[0]} — {loc[1]}", MAGENTA))

        sel = input(warna('Pilih lokasi (nomor) atau ketik `status`/`rest`/`quit`: ', CYAN)).strip().lower()
        if sel == 'status':
            status(player)
            continue
        if sel == 'rest':
            rest_or_use(player)
            continue
        if sel == 'quit':
            cetak(warna('Keluar dari petualangan. Sampai jumpa!', YELLOW))
            break

        try:
            idx = int(sel) - 1
            if 0 <= idx < len(LOCATIONS):
                encounter(player, LOCATIONS[idx])
                # class XP bonus
                if player['cls'] == 'Mage':
                    bonus = 5
                    player['xp'] += bonus
                    cetak(warna(f'Mage bonus: +{bonus} XP', BLUE))

                check_levelup(player)
                if player['hp'] <= 0:
                    cetak(warna('Kau tewas. Akhir perjalanan untuk sekarang.', RED))
                    break
            else:
                cetak('Pilihan tidak valid.')
        except ValueError:
            cetak('Masukkan tidak dimengerti.')

def main():
    cetak(warna('=== Selamat datang di DnD: MisteriAdventure ===', BOLD+CYAN))
    name = input(warna('Masukkan namamu: ', CYAN)).strip() or 'Penjelajah'
    cls = choose_class()
    # base stats by class
    base_hp = 120 if cls == 'Warrior' else 90 if cls == 'Rogue' else 80
    player = {'name': name, 'cls': cls, 'hp': base_hp, 'max_hp': base_hp, 'xp': 0, 'level':1, 'gold':20, 'potions':1}

    while True:
        game_loop(player)
        lagi = input(warna('Main lagi dari awal (reset) atau lanjut dengan karakter yang sama? (reset/continue/quit): ', CYAN)).strip().lower()
        if lagi == 'reset':
            player = {'name': player['name'], 'cls': player['cls'], 'hp': base_hp, 'max_hp': base_hp, 'xp': 0, 'level':1, 'gold':20, 'potions':1}
            cetak(warna('Permainan direset. Selamat mencoba lagi!', YELLOW))
            continue
        if lagi == 'continue':
            cetak(warna('Melanjutkan dengan status saat ini...', GREEN))
            continue
        break

if __name__ == '__main__':
    main()
