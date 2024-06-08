import pygame
import random
import sys
import itertools
# 파이게임 및 믹서 초기화
pygame.init()
pygame.mixer.init()

main_menu_music = 'SellBuyMusic - 해변의 저녁.mp3'
game_music = 'SellBuyMusic - 밝은 하우스 브금.mp3'
PlayerWin_music = '롤 - 승리.mp3'
AiWin_music = '블리츠크랭크 - 인간시대의 끝이.mp3'
HomeRun_misic = "Small Crowd Applause Sound.mp3"

def play_background_music(music):
    pygame.mixer.music.stop()  # 현재 재생 중인 음악 정지
    pygame.mixer.music.load(music)  # 새 음악 로드
    pygame.mixer.music.play(-1)  # 음악 무한 반복 재생

# 화면 설정
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("숫자 야구 게임")

# 색 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 69, 0)
GREEN = (34, 139, 34)
DARK_GRAY = (169, 169, 169)
LIGHT_GRAY = (211, 211, 211)

# 폰트 로드
font_path = "NanumGothic.ttf"
font = pygame.font.Font(font_path, 36)
small_font = pygame.font.Font(font_path, 24)
button_font = pygame.font.Font(font_path, 30)

# 폰트 로드
font_path2 = "NanumGothic-Bold.ttf"
font2 = pygame.font.Font(font_path, 48)
small_font2 = pygame.font.Font(font_path, 24)
button_font2 = pygame.font.Font(font_path, 30)


# 무작위 숫자 생성 : AI의 추측 숫자로 사용
def generate_random_number(length, unique):
    numbers = list(range(10))
    if unique:
        return ''.join(str(numbers.pop(random.randint(0, len(numbers)-1))) for _ in range(length))
       # 임의의 수를 게임 설정에 맞게 반복해서 생성, 중복을 제거하기 위해 pop사용, 이후 리스트 결과를 join으로 문자열로 결합
    else:
        return ''.join(str(random.choice(numbers)) for _ in range(length))
        # 중복을 허용한 수 생성, pop을 사용안함

    #return '1234' # 게임테스트 용 숫자


# 숫자 조합 생성 : AI의 추측할 숫자 후보들 생성
def generate_combinations(length, unique):
    digits = '0123456789'
    if unique:
        return [''.join(comb) for comb in itertools.permutations(digits, length)]
        # itertools.permutations로 중복 불가
    else:
        return [''.join(comb) for comb in itertools.product(digits, repeat=length)]
        # itertools.product로 중복 가능

# 점수 계산
def calculate_score(secret, guess):
    strike = 0
    ball = 0
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            strike += 1
        elif guess[i] in secret:
            ball += 1
    return strike, ball

# 후보 숫자 필터링
def filter_candidates(candidates, guess, strike, ball): # 파라미터 : 후보 숫자들, 이전 추측, 이전 스트라이크 후, 이전 볼 수
    return [candidate for candidate in candidates if calculate_score(candidate, guess) == (strike, ball)]
    #조건문으로 후보와 추측 간의 스트라이크와 볼수를 계산해서 계산된 스트라이크랑 볼 수랑 같다면
    #해당 candidate를 결과 리스트에 포함시킨다.
    #에를 들어, 후보군에 1234, 5678, 1243, 4321이 있고 추측에 1234가 있고 스트라이크에는 1, 볼에는 2가 있다면
    # calculate_score("5678", "1234") 호출이 되면
    # 스트라이크: 0.
    # 볼: 0.
    # 조건 검사: (0, 0) == (1, 2) -> 거짓이므로
    # "5678"는 결과 리스트에 포함되지 않는다.'

    # calculate_score("1243", "1234") 호출이 되면
    # 스트라이크: 1 (첫 번째 자리 1이 일치).
    # 볼: 2 (2와 3이 일치하지만 자리가 다름).
    # 조건 검사: (1, 2) == (1, 2) -> 참이므로
    # "1243"는 결과 리스트에 포함된다.




# AI 클래스 정의
class NumberBaseballAI:
    def __init__(self, length, unique, difficulty): #게임의 설정 초기화
        self.length = length # 숫자의 길이
        self.unique = unique # 중복숫자여부
        self.difficulty = difficulty #난이도
         # 가능한 모든 숫자 조합을 생성하여 후보 숫자 목록, 즉 AI가 현재 고려하고 있는 후보 숫자 목록
        self.candidates = generate_combinations(length, unique)
        self.history = [] # AI의 추측 기록을 저장하는 리스트
    
    def make_guess(self):
        if self.difficulty == "쉬움":
            return self.make_guess_easy()
        elif self.difficulty == "보통":
            return self.make_guess_middle()
        elif self.difficulty == "어려움":
            return self.make_guess_hard()
    #
    def make_guess_easy(self):
        if random.random() < 0.5:  # 50% 확률로 무작위 추측
            return generate_random_number(self.length, self.unique)
        
        if self.history: # 이전 추측 결과를 저장한 리스트, 비어있지 않다면
            last_guess, last_strike, last_ball = self.history[-1] #마지막 추측의 결과를 가져와서
            possible_candidates = [g for g in self.candidates if calculate_score(g, last_guess) == (last_strike, last_ball)]
            # 현재 후보군인 self.candidates에서 마지막 추측 같은 스트라이크와 볼 결과를 갖는 후보들만 필터링하여 possible_candidates 리스트에 저장
            if possible_candidates:
                self.candidates = possible_candidates
            else:
                self.candidates = generate_combinations(self.length, self.unique)
        return random.choice(self.candidates) if self.candidates else generate_random_number(self.length, self.unique)
                # 후보 목록이 비워져 있지 않다면, random.choice(self.candidates)후보군에서 암거나 선택
    
    def make_guess_middle(self):
        # 힌트를 덜 효과적으로 사용하도록 무작위성을 추가
        if random.random() < 0.3:  # 30% 확률로 무작위 추측, 쉬움 난이도와 성능차이를 위해
            return generate_random_number(self.length, self.unique)
        
        if self.history: # 이전 추측 결과를 저장한 리스트
            last_guess, strike, ball = self.history[-1]
            # 일부 힌트를 무시하고 필터링
            possible_candidates = [g for g in self.candidates if calculate_score(g, last_guess) == (strike, ball)]
            if possible_candidates:
                self.candidates = possible_candidates
            else:
                self.candidates = generate_combinations(self.length, self.unique)
        
        return random.choice(self.candidates) if self.candidates else generate_random_number(self.length, self.unique)
    
    def make_guess_hard(self):
        # if random.random() <  0:  # 0% 확률로 무작위 추측, 없어도 되기에 주석처리
        #     return generate_random_number(self.length, self.unique)

        if self.history:
            last_guess, last_strike, last_ball = self.history[-1]
            possible_candidates = [g for g in self.candidates if calculate_score(g, last_guess) == (last_strike, last_ball)]
            if possible_candidates:
                self.candidates = possible_candidates
            else:
                self.candidates = generate_combinations(self.length, self.unique)
        return random.choice(self.candidates) if self.candidates else generate_random_number(self.length, self.unique)
    
    def receive_feedback(self, guess, strike, ball):
        self.history.append((guess, strike, ball))

# 메인 메뉴
def main_menu():
    play_background_music(main_menu_music) #배경음악 실행
    while True:
        win.fill(WHITE)
        draw_text('숫자 야구 게임', font, BLACK, win, 250, 100)
        draw_button('컴퓨터와 대결', button_font, BLACK, win, 250, 200, 300, 50)
        draw_button('종료', button_font, BLACK, win, 250, 300, 300, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #마우스로 버튼 클릭하도록
                if 250 <= event.pos[0] <= 550:
                    if 200 <= event.pos[1] <= 250:
                        select_difficulty() # 컴퓨터와 대결 선택 버튼 위치, 클릭 시 난이도 선택으로
                    elif 300 <= event.pos[1] <= 350:
                        pygame.quit()
                        sys.exit()

# 텍스트 및 버튼 그리기 함수
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)# 텍스트 객체 랜더링하고
    textrect = textobj.get_rect() #사각형 영역을 가져와서
    textrect.topleft = (x, y) # 왼쪽상단 모서리 좌표설정
    surface.blit(textobj, textrect) # 화면에 그리기

def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, LIGHT_GRAY, (x, y, width, height)) # 버튼 배경
    pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height), 3) #버튼 테두리
    draw_text(text, font, color, surface, x + 20, y + 10) # 버튼 텍스트

# 게임 시작 및 난이도 선택
def select_difficulty():
    while True:
        win.fill(WHITE)
        draw_text('난이도 선택:', font, BLACK, win, 250, 100)
        draw_button('쉬움', button_font, BLUE, win, 250, 200, 300, 50)
        draw_button('보통', button_font, GREEN, win, 250, 300, 300, 50)
        draw_button('어려움', button_font, RED, win, 250, 400, 300, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 550:
                    if 200 <= event.pos[1] <= 250:
                        game_settings("쉬움")
                    elif 300 <= event.pos[1] <= 350:
                        game_settings("보통")
                    elif 400 <= event.pos[1] <= 450:
                        game_settings("어려움")

# 게임 설정 함수
def game_settings(difficulty):
    length = 4 # 디폴트로 4자리
    unique = True # 디폴트로 중복 수는 불가
    while True:
        win.fill(WHITE)
        draw_text('숫자의 길이를 선택하세요 (4-8):', small_font, BLACK, win, 100, 100) 
        draw_text(f'현재 길이: {length}', small_font, BLACK, win, 100, 150)
        draw_text('중복 숫자 허용: U 키로 전환 (예/아니오)', small_font, BLACK, win, 100, 200)
        draw_text(f'중복 숫자 허용 여부: {"예" if not unique else "아니오"}', small_font, BLACK, win, 100, 250)
        draw_text('계속하려면 Enter 키를 누르세요', small_font, BLACK, win, 100, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # up,down 키로 숫자 자리수 설정
                if event.key == pygame.K_UP:
                    if length < 8:
                        length += 1
                if event.key == pygame.K_DOWN:
                    if length > 4:
                        length -= 1
                if event.key == pygame.K_u: #  u키 로 중복 여부 설정
                    unique = not unique
                if event.key == pygame.K_RETURN:
                    enter_secret_numbers(length, unique, difficulty) # 다음 화면인 숫자 설정 화면으로

# 플레이어 비밀 번호 입력 함수
def enter_secret_numbers(length, unique, difficulty):
    player_secret = ""
    ai_secret = generate_random_number(length, unique) # AI 비밀번호 생성
    warning_text = ""
    win.fill(WHITE)
    draw_text('비밀 번호를 입력하세요:', small_font, BLACK, win, 100, 100)
    pygame.display.update()

    while len(player_secret) < length: #플레이어가 설정한 숫자 자리 만큼 입력할 때까지 무한루프
        for event in pygame.event.get(): # Pygame 이벤트 큐에서 발생한 모든 이벤트를 처리, 여기서 각 이벤트를 순회
            if event.type == pygame.QUIT: # 갑자기 게임을 나가면
                pygame.quit()
                sys.exit() #다 종료
            if event.type == pygame.KEYDOWN: #키 눌림 감지
                if event.key == pygame.K_BACKSPACE: #백스페이스 감지 시
                    player_secret = player_secret[:-1] # 하나 지우기
                elif event.unicode.isdigit() and (not unique or event.unicode not in player_secret): # 누른 키가 숫자인지 확인, 중복이 안되는 경우 중복 검사
                    player_secret += event.unicode
                else:
                    warning_text = "숫자는 중복될 수 없습니다!"

        win.fill(WHITE)
        draw_text('비밀 번호를 입력하세요:', small_font, BLACK, win, 100, 100)
        draw_text(player_secret, font, BLACK, win, 300, 100)
        draw_text(warning_text, small_font, RED, win, 100, 200)
        pygame.display.update()

    play_game(length, unique, player_secret, ai_secret, difficulty) #게임 플레이로

# 만일 4번만에 맞춰 이긴다면....홈런!
def game_over_HomeRun_screen(winner, ai_secret):
    pygame.mixer.music.stop()  # 배경 음악 정지
    pygame.mixer.music.load(HomeRun_misic)
    pygame.mixer.music.play()  # 승리 음악 재생
    while True:  # 게임 오버 화면 이벤트 루프
        win.fill(WHITE)
        draw_text('홈런!!!', font2, GREEN, win, 350, 100)
        draw_text('완승!!', font, RED, win, 300, 250)
        draw_text(f'AI 비밀 번호: {ai_secret}', small_font, BLACK, win, 250, 300)
        draw_button('다시 하기', button_font, BLACK, win, 250, 350, 300, 50)
        draw_button('종료', button_font, BLACK, win, 250, 450, 300, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 550 and 350 <= event.pos[1] <= 400:
                    main_menu()  # 메인 메뉴로 복귀
                elif 250 <= event.pos[0] <= 550 and 450 <= event.pos[1] <= 500:
                    pygame.quit()
                    sys.exit()

# 게임 종료 화면 함수
def game_over_screen(winner, ai_secret ):
    pygame.mixer.music.stop()  # 배경 음악 정지
    if winner == "player":
        pygame.mixer.music.load(PlayerWin_music)
        pygame.mixer.music.play()  # 승리 음악 재생
        while True:  # 게임 오버 화면 이벤트 루프
            win.fill(WHITE)
            draw_text('승리!', font, RED, win, 300, 250)
            draw_text(f'AI 비밀 번호: {ai_secret}', small_font, BLACK, win, 250, 300)
            draw_button('다시 하기', button_font, BLACK, win, 250, 350, 300, 50)
            draw_button('종료', button_font, BLACK, win, 250, 450, 300, 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 250 <= event.pos[0] <= 550 and 350 <= event.pos[1] <= 400:
                        main_menu()  # 메인 메뉴로 복귀
                    elif 250 <= event.pos[0] <= 550 and 450 <= event.pos[1] <= 500:
                        pygame.quit()
                        sys.exit()
                    pygame.display.update()  # 화면 업데이트
    else:
        pygame.mixer.music.load(AiWin_music)
        pygame.mixer.music.play()  # AI 승리 음악 재생
        while True:  # 게임 오버 화면 이벤트 루프
            win.fill(WHITE)
            draw_text('패배!', font, RED, win, 300, 250)
            draw_text(f'AI 비밀 번호: {ai_secret}', small_font, BLACK, win, 250, 300)
            draw_button('다시 하기', button_font, BLACK, win, 250, 350, 300, 50)
            draw_button('종료', button_font, BLACK, win, 250, 450, 300, 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 250 <= event.pos[0] <= 550 and 350 <= event.pos[1] <= 400:
                        main_menu()  # 메인 메뉴로 복귀
                    elif 250 <= event.pos[0] <= 550 and 450 <= event.pos[1] <= 500:
                        pygame.quit()
                        sys.exit()
                    pygame.display.update()  # 화면 업데이트

# 게임 플레이 함수
def play_game(length, unique, player_secret, ai_secret, difficulty):
    play_background_music(game_music)
    guess = ""
    attempts = 0
    ai_attempts = 0
    player_guesses = []
    ai_feedback = []
    result_text = ""
    ai_result_text = ""
    warning_text = ""

    player_records = []
    ai_records = []

    # AI 초기화
    ai = NumberBaseballAI(length, unique, difficulty)

    while True: # 게임 루프
        win.fill(WHITE) # 게임 화면 설정
        draw_text(f'플레이어: {player_secret}', small_font, BLACK, win, 100, 50)
        draw_text(f'AI: {"*" * length}', small_font, BLACK, win, 500, 50)
        draw_text('추측 번호를 입력하세요:', small_font, BLACK, win, 100, 100)
        draw_text(guess, font, BLACK, win, 300, 150)
        draw_text(result_text, small_font, BLACK, win, 100, 200)
        draw_text(ai_result_text, small_font, BLACK, win, 500, 200)
        draw_text(warning_text, small_font, RED, win, 100, 250)

        #플레이어 추측 기록 표시
        y_offset = 300
        for record in player_records:
            draw_text(record, small_font, BLUE, win, 100, y_offset)
            y_offset += 30 #다음 기록을 위해 y좌표를 증가
        # AI 추측 기록 표시
        y_offset = 300
        for record in ai_records:
            draw_text(record, small_font, RED, win, 500, y_offset)
            y_offset += 30

        pygame.display.update() #화면 업데이트


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(guess) == length:
                        if unique and len(set(guess)) != length:
                            warning_text = "숫자는 중복될 수 없습니다!"
                        else:
                            attempts += 1
                            strike, ball = calculate_score(ai_secret, guess) #스트라이크 볼 계산
                            result_text = f'{strike} 스트라이크, {ball} 볼' # 계산 결과 출력
                            player_records.append(f'{guess}: {strike}S {ball}B') # 플레이어의 추측과 결과 기록
                            player_guesses.append(guess)
                            if len(player_records) > 10:  # 최대 10개의 기록만 유지
                                player_records.pop(0)
                            if strike == length:
                                if attempts < 4: #만일 추측 4번만에 맞춘다면
                                    game_over_HomeRun_screen("player", ai_secret) #홈런!
                                game_over_screen("player", ai_secret)
                               

                            ai_feedback.append((strike, ball)) #AI 추측 기록
                            ai_guess = ai.make_guess() # AI 추측
                            ai.receive_feedback(ai_guess, *calculate_score(player_secret, ai_guess)) # AI의 추측에 대한 내용 기록
                            ai_attempts += 1
                            ai_strike, ai_ball = calculate_score(player_secret, ai_guess) # 추측 결과 계산
                            ai_result_text = f'{ai_guess} : {ai_strike} S, {ai_ball} B' # 결과 출력
                            ai_records.append(f'{ai_guess}: {ai_strike}S {ai_ball}B') # 기록하기
                            if len(ai_records) > 10:  # 최대 10개의 기록만 유지
                                ai_records.pop(0)
                            if ai_strike == length:
                                game_over_screen("ai", ai_secret)
                                

                            guess = ""
                            warning_text = ""
                elif len(guess) < length and event.unicode.isdigit() and (not unique or event.unicode not in guess):
                    guess += event.unicode
                    #현재 추측의 길이가 지정된 길이보다 작거나 입력된 키가 숫자인지 확인하며, 고유한 숫자가 필요한 경우 중복되지 않은 숫자인지 확인

if __name__ == "__main__":
    main_menu()
