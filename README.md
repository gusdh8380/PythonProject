# 숫자 야구 게임

이 프로젝트는 Python과 Pygame을 사용하여 만든 숫자 야구 게임입니다. 플레이어는 컴퓨터와 숫자 야구 게임을 플레이하며, 난이도에 따라 AI와 경쟁합니다.

## 게임 설명

숫자 야구 게임은 비밀 번호를 맞추는 게임입니다. 플레이어와 컴퓨터는 각각 비밀 번호를 설정하고, 상대의 비밀 번호를 추측합니다. 각 추측에 대해 스트라이크와 볼의 수를 알려줍니다.

- **스트라이크**: 숫자와 위치가 모두 맞는 경우
- **볼**: 숫자는 맞지만 위치가 다른 경우

## 실행 방법

1. **스크립트 실행**
   - 다음 명령어를 통해 게임을 실행합니다.
     ```bash
     python GamePJ2.py
     ```
     
2. **메인 메뉴**
   - 게임을 실행하면 메인 메뉴가 표시됩니다.
   - "컴퓨터와 대결" 버튼을 클릭하여 게임을 시작하거나, "종료" 버튼을 클릭하여 게임을 종료합니다.

3. **난이도 선택**
   - 난이도 선택 화면에서 "쉬움", "보통", "어려움" 중 하나를 선택합니다.

4. **게임 설정**
   - 숫자의 길이와 중복 숫자 허용 여부를 설정합니다.
   - 설정이 완료되면 비밀 번호를 입력합니다.

5. **게임 플레이**
   - 플레이어는 추측 번호를 입력하고, 컴퓨터와 번갈아가며 추측합니다.
   - 각 추측에 대해 스트라이크와 볼의 수를 확인할 수 있습니다.

## 파일 설명

- **GamePJ2.py**: 게임의 메인 코드가 포함된 파일입니다.
- **NanumGothic.ttf**: 게임에 사용되는 폰트 파일입니다. (필요시 폰트 파일을 프로젝트 디렉토리에 포함시킵니다.)


