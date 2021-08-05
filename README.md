# MLTD Deck Analyzer

## Info / 정보

for THE iDOLM@STER MILLION LIVE! THEATER DAYS / MLTD

for アイドルマスター ミリオンライブ！ シアターデイズ / ミリシタ

for 아이돌 마스터 밀리언 라이브! 시어터 데이즈 / 밀리시타

Automatic High Score Deck Making / 가장 높은 점수를 내는 덱을 찾아주는 덱 최적화 프로그램

## How to Use / 사용 방법

### Update from older version / 이전 버전에서 업데이트

#### Exe Version / Exe 버전에서

Copy mltdkei_info.txt or mltdkei_info_kr.txt from older version folder and paste them to newer version folder. Then run Update DB > Card.

기존 버전 프로그램 폴더 내부의 mltdkei_info.txt 혹은 mltdkei_info_kr.txt 를 복사해서 새로운 버전 프로그램 폴더 내부에 붙여넣어준 후 Update DB의 Card 를 실행합니다.

#### pypy Version / pypy 버전에서

Download code.7z, extract and change "code" folder to newer one.

code.7z 파일을 내려받아 압축을 푼 후, 기존 프로그램 폴더 내부의 "code" 폴더를 새로 다운로드 받은 폴더로 교체합니다.

### Main Setting / 기본 설정

- Live Type: Select PSTheater type bonus / PSTheater(시어터) 타입 보너스 유무 결정
- Deck Mode: Select prefered leader idol's skill type / 우선시할 리더 아이돌의 리더 스킬 결정
  - "ST+3T" is "Songtype"+"3Type". You can compare results from two option at once. / "ST+3T"는 "Songtype"+"3Type"를 의미합니다. 각각의 옵션으로 만든 덱을 한번에 비교할 수 있습니다.
- Deck Type: Select prefered appeal value type(between Vo, Da, Vi) / 우선시할 어필치 종류를 선택(보컬, 댄스, 비주얼 중에서)
- Order By: Select how to order the results. You can rearrange them after calculation. / 결과 정렬 방식 결정, 계산 이후에 정렬 방법을 바꿀 수 있습니다.
- Update DB: Update DB when there is card or song update. / 카드 혹은 수록곡 갱신 시 업데이트 가능
  - It is recommended to update both after updating from older version or downloading first. / 이전 버전에서 업데이트 시 혹은 새로 다운로드 받은 후에 둘 다 한번은 업데이트 해 주는 것을 권장합니다.
  - When program gets some error, try updating both file. In most case it will solve them. / 프로그램에 에러 발생 시, 두 파일을 모두 업데이트 해 보기를 권장합니다. 대부분 해결됩니다.
- Config Idol List: Edit your current idol list / 현재 보유하고 있는 아이돌 목록을 편집
  - You can change all of idols' status shown on window with third line of buttons. / 3번째 줄의 버튼을 이용하면, 화면에 보이는 모든 아이돌의 설정 상태를 바꿀 수 있습니다.
  - Press save button before closing window, unless you will lose your all changes. / 창을 닫기 전에 세이브 버튼을 눌러 꼭 저장하세요. 창을 그냥 닫으면 편집된 내용이 저장되지 않습니다.

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

Special Thanks to megmeg_work, hiside0, Baby_Rabbit, karl**** from MLTD-KR Naver Cafe

이미지가 첨부된 한글 매뉴얼은 이쪽으로 https://gall.dcinside.com/mgallery/board/view/?id=theaterdays&no=5354535
