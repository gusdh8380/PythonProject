import random
import itertools
from collections import Counter

# 필요한 함수들 정의
def generate_random_number(length, unique=True):
    numbers = list(range(10))
    if unique:
        return ''.join(str(numbers.pop(random.randint(0, len(numbers) - 1))) for _ in range(length))

def calculate_score(secret, guess):
    strike = 0
    ball = 0
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            strike += 1
        elif guess[i] in secret:
            ball += 1
    return strike, ball

def generate_combinations(length, unique=True):
    digits = '0123456789'
    if unique:
        return [''.join(comb) for comb in itertools.permutations(digits, length)]

def filter_candidates(candidates, guess, strike, ball):
    return [candidate for candidate in candidates if calculate_score(candidate, guess) == (strike, ball)]

class NumberBaseballAI:
    def __init__(self, length, unique, difficulty):
        self.length = length
        self.unique = unique
        self.difficulty = difficulty
        self.candidates = generate_combinations(length, unique)
        self.history = []

    def make_guess(self):
        if self.difficulty == "쉬움":
            return self.make_guess_easy()
        elif self.difficulty == "어려움":
            return self.make_guess_hard()
        elif self.difficulty == "중간":
            return self.make_guess_middle()

    def make_guess_easy(self):
        if random.random() < 0.5:  # 50% 확률로 무작위 추측
            return generate_random_number(self.length, self.unique)
        if self.history:
            last_guess, last_strike, last_ball = self.history[-1]
            possible_candidates = [g for g in self.candidates if calculate_score(g, last_guess) == (last_strike, last_ball)]
            if possible_candidates:
                self.candidates = possible_candidates
            else:
                self.candidates = generate_combinations(self.length, self.unique)
        return random.choice(self.candidates) if self.candidates else generate_random_number(self.length, self.unique)
    
    def make_guess_hard(self):
        
        if self.history:
            last_guess, last_strike, last_ball = self.history[-1]
            possible_candidates = [g for g in self.candidates if calculate_score(g, last_guess) == (last_strike, last_ball)]
            if possible_candidates:
                self.candidates = possible_candidates
            else:
                self.candidates = generate_combinations(self.length, self.unique)
        return random.choice(self.candidates) if self.candidates else generate_random_number(self.length, self.unique)
    
    def make_guess_middle(self):
        if random.random() < 0.3:  # 30% 확률로 무작위 추측
            return generate_random_number(self.length, self.unique)
        
        if self.history:
            last_guess, strike, ball = self.history[-1]
            # 일부 힌트를 무시하고 필터링
            possible_candidates = [g for g in self.candidates if calculate_score(g, last_guess) == (strike, ball)]
            if possible_candidates:
                self.candidates = possible_candidates
            else:
                self.candidates = generate_combinations(self.length, self.unique)
        
        # 무작위 추측을 더 많이 포함
        guess = random.choice(self.candidates) if self.candidates else generate_random_number(self.length, self.unique)
        return guess

   
    
    def receive_feedback(self, guess, strike, ball):
        self.history.append((guess, strike, ball))

# 테스트 케이스 생성
test_numbers = [generate_random_number(4) for _ in range(100)]

# 난이도별 AI 성능 테스트
difficulties = ["쉬움", "어려움", "중간"]
results = {difficulty: [] for difficulty in difficulties}

for difficulty in difficulties:
    print(f"Testing {difficulty} difficulty...")
    for secret_number in test_numbers:
        ai = NumberBaseballAI(4, True, difficulty)
        attempts = 0
        while True:
            attempts += 1
            guess = ai.make_guess()
            strike, ball = calculate_score(secret_number, guess)
            ai.receive_feedback(guess, strike, ball)
            if strike == 4:
                break
        results[difficulty].append(attempts)

# 평균 시도 횟수 계산 및 출력
for difficulty in difficulties:
    average_attempts = sum(results[difficulty]) / len(results[difficulty])
    print(f"{difficulty} Difficulty: Average {average_attempts:.2f} attempts to guess correctly.")
