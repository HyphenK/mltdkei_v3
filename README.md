# MLTD Deck Analyzer

## Info / 정보

for THE iDOLM@STER MILLION LIVE! THEATER DAYS / MLTD

for アイドルマスター ミリオンライブ！ シアターデイズ / ミリシタ

for 아이돌 마스터 밀리언 라이브! 시어터 데이즈 / 밀리시타

Automatic High Score Deck Making / 가장 높은 점수를 내는 덱을 찾아주는 덱 최적화 프로그램

## How to Use / 사용 방법

### Update from older version / 이전 버전에서 업데이트

Copy mltdkei_info.txt or mltdkei_info_kr.txt from older version folder and paste them to newer version folder. Then run Update DB > Card.

기존 버전 프로그램 폴더 내부의 mltdkei_info.txt 혹은 mltdkei_info_kr.txt 를 복사해서 새로운 버전 프로그램 폴더 내부에 붙여넣어준 후 Update DB의 Card 를 실행합니다.

### Main Setting / 기본 설정

- Live Type: Select PSTheater type bonus / PSTheater(시어터) 타입 보너스 유무 결정
- Deck Mode: Select prefered leader idol's skill type / 우선시할 리더 아이돌의 리더 스킬 결정
  - Options without "+" select only one leader idol for similar leader skill group. / 뒤에 "+"가 없는 옵션을 선택하면, 비슷한 리더 스킬 그룹에서 한 명의 아이돌만 리더로 선택됩니다.
  - Options with "+" select each of leader idol for each of leader skill. / 뒤에 "+"가 있는 옵션을 선택하면, 리더 스킬당 한 명의 아이돌을 리더로 선택합니다.
- Deck Type: Select prefered appeal value type(between Vo, Da, Vi) / 우선시할 어필치 종류를 선택(보컬, 댄스, 비주얼 중에서)
- Order By: Select how to order the results. You can rearrange them after calculation. / 결과 정렬 방식 결정, 계산 이후에 정렬 방법을 바꿀 수 있습니다.
- Update DB: Update DB when there is card or song update. / 카드 혹은 수록곡 갱신 시 업데이트 가능
  - It is recommended to update both after updating from older version or downloading first. / 이전 버전에서 업데이트 시 혹은 새로 다운로드 받은 후에 둘 다 한번은 업데이트 해 주는 것을 권장합니다.
  - When program gets some error, try updating both file. In most case it will solve them. / 프로그램에 에러 발생 시, 두 파일을 모두 업데이트 해 보기를 권장합니다. 대부분 해결됩니다.
  - DB file Update can be a bit delayed due to some handwork. / 수작업으로 진행하기 때문에, DB 파일 업데이트가 약간 늦어질 수 있습니다.
- Config Idol List: Edit your current idol list / 현재 보유하고 있는 아이돌 목록을 편집
  - You can change all of idols' status shown on window with third line of buttons. / 3번째 줄의 버튼을 이용하면, 화면에 보이는 모든 아이돌의 설정 상태를 바꿀 수 있습니다.
  - Don't forget to save before closing windows, unless you will lose your all changes. / 창을 닫기 전에 세이브 버튼을 눌러 꼭 저장하세요. 창을 그냥 닫으면 편집된 내용이 저장되지 않습니다.

### Presets Description / 프리셋

- Default: For beginners who has less SSR+ cards / SSR+ 카드 소지 수가 적은 초심자용
- Light: For fast result, may not be accurate / 빠른 결과를 내는 용, 결과가 정확하지 않을 수 있음
- Accurate: For intermediates who can make almost full SSR+ support decks / 서포트 덱을 거의 전부 SSR+로 채울 수 있을 정도로 SSR+ 카드를 보유한 중급자용
- All Max: Suppose all of your current idols are max rank and max skill level / 현재 보유한 모든 아이돌의 능력치가 최대일 때의 결과 분석
- Theoretical: Find the theoretical maximum score in the game / 현재 게임상에서 가능한 최상의 결과 분석

### Advanced Setting / 고급 설정

- Combination: Select the number of idols for deck building, ordered by total appeal values / 덱 구성 시에 사용할 아이돌 수 설정, 어필치 순서대로 선택됨
  - If you get unsatisfying results or "Cannot make any deck under this option" error message, try increasing this value. / 결과가 만족스럽지 않거나 "Cannot make any deck under this option" 에러 메세지가 뜨는 경우, 이 값을 더 높은 값으로 설정해 보세요.
- Ideal Calc: Select the number of decks for maximum score calculation, ordered by decks' total appeal values / 최상의 점수를 계산할 덱 개수 설정, 각 덱 전체의 어필치 순서대로 선택됨
- Score Calc: Select the number of decks for real score calculation, ordered by deck's maximum score / 실제 스킬 발동 확률을 적용한 시뮬레이션을 진행할 덱 개수 설정, 각 덱의 최상의 점수 순서대로 선택됨
- Time of Calc: Select the number of score calculation for each "Score Calc" deck / 각 "Score Calc" 덱의 시뮬레이션 횟수 설정
- Unit Maiking Mode: Select "Legacy" when you get "Cannot make any deck under this option" error message after increasing "Combination" option. / "Combination" 옵션을 더 높게 설정해도 "Cannot make any deck under this option" 에러 메세지가 뜨는 경우, "Legacy" 로 설정하세요.
- Manual Leader Select: Activates manual leader selection / 수동 리더 아이돌 설정 기능 활성화
  - When enabled and the leader idol is selected, the program will ignore "Deck Mode" and "Deck Type" option and create deck by leader skill of selected leader idol. / 이 옵션이 활성화되고 리더 아이돌이 선택되어 있을 경우, "Deck Mode"와 "Deck Type" 옵션을 무시하고 선택된 아이돌의 리더 스킬에 의해서만 덱이 만들어집니다.
  - When disabled, the program will act as normal and select leader automatically even if there is selected leader idol. / 이 옵션이 비활성화되었을 경우, 리더 아이돌이 선택되어 있어도 이것을 무시하고 프로그램의 기본 세팅대로 작동합니다.

## Others / 기타

This program uses data from https://mltd.matsurihi.me/cards and https://imasml-theater-wiki.gamerch.com/%E6%A5%BD%E6%9B%B2%E4%B8%80%E8%A6%A7

이 프로그램은 위에 적어놓은 두 사이트의 데이터를 사용합니다.

Special Thanks to megmeg_work, hiside0, Baby_Rabbit, karl**** from MLTD-KR Naver Cafe
