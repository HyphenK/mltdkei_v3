# MLTD Deck Analyzer

for THE iDOLM@STER MILLION LIVE! THEATER DAYS (MLTD)

アイドルマスター ミリオンライブ！ シアターデイズ (ミリシタ)

아이돌 마스터 밀리언 라이브! 시어터 데이즈 (밀리시타)

## 할 수 있는 거 (Features)

하이스코어용 덱 만들기 (Deck Making for Scoring)

덱별 스코어 계산 (Score Calculating)

소지 카드 현황 한눈에 보기 (Card Statistics)

## 시스템 요구 사항 (System Requirements)

### 최소 사양 (Minimum Specification)

- OS: Windows 10
- CPU: CPU with 4 Threads / 4쓰레드 이상 CPU (셀러론 같은 거 안됨)
- RAM: 8 GB

### 권장 사양 (Recommended Specification)

- OS: Windows 10
- CPU: CPU with 8 Threads / 8쓰레드 이상 CPU
- RAM: 16 GB

## 기본 사용 방법 (How to Use - Basic)

### 한국어

1. DB 업데이트를 합니다. 업데이트 탭에서 파일 업데이트 유무를 확인할 수 있습니다.
2. 가지고 있는 카드를 소지 카드 리스트에 넣어줍니다. 스코어 계산만이 목적이라면 SSR 등급과 PST SR 등급 카드만 넣어줘도 됩니다.
3. 노래 타입과 제목, 이벤트 옵션과 덱 조합 방법, 프리셋을 설정한 후 시작 버튼을 누릅니다.
4. 잠시 기다리면 계산 소요시간과 함께 결과가 표출됩니다. 너무 오래 걸린다면 프리셋을 낮은 단계로 바꾸거나 아래의 상세 사용 설정을 참고하여 옵션을 바꿔보세요.

#### 소지 카드 리스트 편집

- 원하는 옵션을 선택한 후 좌측 상단의 "Load" 버튼을 눌러 카드 리스트를 불러옵니다.
- 편집을 마친 후에는 반드시 좌측 상단의 "Save" 버튼을 눌러 저장하시기 바랍니다. 창을 그냥 닫으면 변경 내용이 저장되지 않습니다.
- 우측 상단 "Config All" 버튼을 눌러 화면에 나와있는 모든 아이돌 카드를 지정하는 상태로 바꿀 수 있습니다.
- 첫번째 탭 하단 의상 항목은 선택 시 다른 옵션을 만족하는 **선택된 의상의 카드만 표시**됩니다.
- 추가되었으면 하는 의상/모음집은 issue에 적어주세요. (1차 송포유 추가 예정)

#### 덱 조합 방법 (옵션 이름: Deck Mode)

- Songtype: 선택된 노래와 일치하는 단속성 덱 제작
- 3Type: 트리콜 리더를 사용한 3속성 덱 제작
- All: Songtype 옵션과 3Type 옵션을 둘 다 사용하여 덱 제작

#### 프리셋 설정

- Beginner: 초심자 모드 (SSR+ 카드 20개 이하 보유 시 권장)
- Advanced: 중급자 모드 (SSR+ 카드 35개 이하 보유 시 권장)
- Expert: 상급자 모드 (SSR+ 카드 50개 이하 보유 시 권장)
- Ranker: 고인물/스코어랭커 모드 (SSR+ 카드 50개 이상 보유 시 권장)
- Theory: 현재 게임에서 만들 수 있는 최상의 스코어 찾기용

#### 계산 결과창

- 중간 부분 탭을 눌러 계산 결과를 저장하고 다른 계산을 하거나, 이미 계산한 것을 불러올 수 있습니다. 최대 8개 저장 가능합니다.
- 아래 부분 왼쪽에서 다른 덱 제작 결과를 확인할 수 있습니다.
- Rearrange By 항목을 이용해 제작된 덱을 다시 정렬할 수 있습니다.

### English

1. Update DB files. You can check at the "Update DB" tab for file updates.
2. Configure the Idol List. If you just want to make decks, inserting only SSR and PST SR cards is enough.
3. Select the Music Type, the Music Name, the Event Bonus, the Deck Options and the Presets, and press the Start button.
4. The result will be shown with the time spent. If it tooks too ong time, lower the presets or change other options explained below.

## 상세 설정 (Advanced Option)

### Presets Description / 프리셋

- Beginner: For beginners who has less SSR+ cards / SSR+ 카드 소지 수가 적은 초심자용
- Intermediate: For intermediates who has about 15 single type SSR+ cards / 15장 정도의 단일 속성 SSR+ 카드를 보유한 중급자용
- Ranker: For rankers who has more than 100 SSR+ cards / SSR+ 카드를 100장 이상 보유한 스코어 랭킹 뛰는 랭커용
- All Max: Suppose all of your current idols are max rank and max skill level / 현재 보유한 모든 아이돌의 능력치가 최대일 때의 결과 분석
- Theoretical: Find the theoretical maximum score in the game / 현재 게임상에서 가능한 최상의 결과 분석

"Ranker" is more accurate, but takes longer to analyze. / "Ranker" 쪽이 더 정확한 결과를 제공하지만, 그만큼 분석에 시간이 더 오래 걸립니다.

### Advanced Setting / 고급 설정

- Using Idols: Select the number of idols for deck building, ordered by total appeal values / 덱 구성 시에 사용할 아이돌 수 설정, 어필치 순서대로 선택됨
  - If you get unsatisfying results, try increasing this value. / 결과가 만족스럽지 않을 경우, 이 값을 더 높은 값으로 설정해 보세요.
- Ideal Calc: Select the number of decks for maximum score calculation, ordered by decks' total appeal values / 최상의 점수를 계산할 덱 개수 설정, 각 덱 전체의 어필치 순서대로 선택됨
- Score Calc: Select the number of decks for real score calculation, ordered by deck's maximum score / 실제 스킬 발동 확률을 적용한 시뮬레이션을 진행할 덱 개수 설정, 각 덱의 최상의 점수 순서대로 선택됨
- Time of Calc: Select the number of score calculation for each "Score Calc" deck / 각 "Score Calc" 덱의 시뮬레이션 횟수 설정
- Deep Calc: Activates "Deep Calc" Mode / 정밀 분석 모드 활성화
  - If enabled, program will select one leader idol for each of leader skill. / 활성화된 경우, 리더 스킬당 한 명의 아이돌이 각각 리더로 선택되어 계산에 활용됩니다.
  - If disabled, program will select only one leader idol for similar leader skill group. / 비활성화된 경우, 비슷한 리더 스킬을 가진 아이돌 중 한 명만 리더로 선택됩니다.

### Manual Leader and Friend Selection / 수동 리더, 프렌드 설정

- When the leader idol is selected, the program will ignore "Deck Mode" and "Deck Type" option and create deck by leader skill of selected leader idol. / 리더 아이돌이 선택되어 있을 경우, "Deck Mode"와 "Deck Type" 옵션을 무시하고 선택된 아이돌의 리더 스킬에 의해서만 덱이 만들어집니다.
- Please press each "reset" button to reset each option. / 설정을 초기화하고 싶을 때는 "reset" 버튼을 눌러주세요.

## Others / 기타

This program uses data from https://mltd.matsurihi.me/cards and https://imasml-theater-wiki.gamerch.com/%E6%A5%BD%E6%9B%B2%E4%B8%80%E8%A6%A7

이 프로그램은 위에 적어놓은 두 사이트의 데이터를 사용합니다.

Idea from megmeg_work, hiside0

Special Thanks to Baby_Rabbit, 정채여니 (https://www.twitch.tv/hhh851104/)
