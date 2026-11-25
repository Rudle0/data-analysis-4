# ====================================
# 01단원. 데이터분석이란 - "이걸 왜 배우냐"
# ====================================
import csv  # csv 파일을 줄 칸으로 끊어 읽어주는 파이썬 기본 모듈
import os  # 파일 경로를 다루는 파이썬 기본 모듈


def dp(name):
    """
    실행 위치가 어디든 data 폴더를 찾아주는 작은 도우미 함수
    "data/17_열처리.csv" 지금 있는 폴더 아래의 data를 뜻함.
    그래서 터미널이 어느 폴더에 서 있느냐에 따라 같은 코드가 되기도 하고
    FileNotFoundError가 나기도 합니다.
    폴더 배치 data-analysis-4/data 밑에 있음
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for c in (
        os.path.join("data", name),
        os.path.join(here, "data", name),
        os.path.join(here, "..", "data", name),
    ):
        if os.path.exists(c):
            return c
    return os.path.join("data", name)


LOT = dp("17_열처리.csv")
PROC = dp("17_열처리_공정.csv")
WIDE = dp("20_cmapss_fd001_sample.csv")

# ====================================
# 0. 오늘 계속 만날 파이썬 표현 7가지
# 전부 1~9 단원에서 배운 것들
# 다만 오늘부터 이 7개 계속 나옵니다.
# ====================================
print("=" * 60)
print("[0] 파이썬 표현 미리 보기")

x = 859.5318  # 실제 온도 평균
print(f"1) {x:.2f} <- .2f=소수 둘째자리")
print(f"   {x:10.1f} <- 10칸 폭")
print(f"   {44:>5d} <- 정수 5칸 오른쪽")
print(f"   {0.0455:.1%} <- 퍼센트로")

with open(LOT, encoding="utf-8-sig") as f:
    r = csv.reader(f)
    header = next(r)  # 첫 줄은 열 이름
    rows = list(r)  # 데이터

temps = [float(row[2]) for row in rows]

print("2) 리스트 컴프리헨션:", temps[:5], "...총", len(temps), "개")
print("3) 조건을 붙이면:", [t for t in temps if t > 862])

pairs = [("온도", 1.39), ("OP값", 13.75), ("CP값", 0.01)]
# 이 세 숫자는 밑에서 할 걸 숫자 열 셋의 '흔들림'을 잰 값
# 여기선 손으로 적어두고, 밑에서 같은 방법으로 다시 재서 맞춰봅니다
print("4) 흔들림 큰 순:", sorted(pairs, key=lambda t: -t[1]))

print("5) 삼항 연산자:", "넓다" if max(temps) - min(temps) > 10 else "좁다")

print("6) 슬라이싱: temps[:3]=", temps[:3])

kinds = {}
for row in rows:
    kinds[row[1]] = kinds.get(row[1], 0) + 1  # get(키, 0) 없으면 0으로 시작
print(
    "7) 딕셔너리로 세기:",
    kinds,
    "| set으로 종류만",
    sorted(set(row[5] for row in rows)),
)


print("=" * 60)
print("[1] 설비 관리 방식이 바뀌어 온 순서")
print("1. 사후보전 - 고장 나면 고친다")
print("2. 예방보전 - 날짜를 정해 미리 교체한다")
print("3. 예지보전 - 숫자를 보고 필요한 때만 정비한다")
# 세 방식이 각각 무엇을 낭비하나
# 사후보전 : 멈춘 시간, 이미 라인이 섰고 납기가 밀렸습니다. 부품값은 가장 적게 드는데 손실은 가장 큽니다.
# 예방보전 : 멀쩡한 부품을 버릴 수도 있음. 날짜를 기준으로 하면 설비의 실제 상태와는 아무 상관이 없거든요.
# ★보통 "예방보전은 안전한 방법"으로 오해함★
# 예지보전 : 이상적으로는 없음. 대신 센서가 붙어있어야 하고, 데이터가 쌓여있어야 하고 그걸 읽을 사람이 있어야함
# ★고장의 징조는 대부분 숫자에 먼저 나타난다★


print("=" * 60)
print("[2] 파일 첫 줄을 그냥 읽으면")
with open(LOT, encoding="utf-8") as f:
    print(" ", repr(f.readline().strip()))

print("열 이름", header)
print("행 수:", len(rows), "/ 열 수:", len(header))
print("첫 줄:", rows[0])

print()
print("[2-1] 상태가 정상이 아닌 줄")
for row in rows:
    if row[5] != "정상":
        print(" ", row)

# 무엇을 묻나                   정답의 생김새           문제의 이름
# 이 설비가 고장 날까?            예/아니오               분류
# 이번에 만든 제품이 불량일까?     불량/양품               분류
# 이 조건면 강도가 얼마나 나올까?  숫자                    회귀
# 지금 뭔가 평소랑 다른가?        정답이 없음             이상탐지


# 4. 데이터 세 종류
# 공정 현장에서 만나는 데이터는 대략 세 종류입니다.
# 1) 센서 시계열 데이터
#    온도, 압력, 진동, 전류를 1분 1초마다 계속 기록한 것
#    우리 파일의 측정시각, 온도, OP값, CP값
#    이 종류의 핵심은 시간 순서가 뜻을 가진다
#    줄 순서를 섞으면 평균을 그대로인데 "오르는 중인지 내리는 중인지"가 사라집니다
# 2) 공전 조건 데이터
#    어떤 설비에서 어떤 모드로 어느 배치로 돌렸는지 같은 설정값
#    우리 파일의 배치(로트A, B, C)
#    이 칸이 분석을 가능하게 만듭니다
# 3) 품질 측정 데이터
#    완성된 제품을 검사한 결과. 합격/불합격, 강도, 열전도율
#    보통 정답, 라벨 역할을 합니다
#    이 칸은 보통 가장 늦게, 가장 적게 쌓입니다.
#    센서는 10분마다 쌓지만 검사는 하루에 몇 번뿐인 경우가 흔함

print("=" * 60)
print("[4] 열 이름과 그 역할, 그리고 값의 종류 수")
roles = {
    "측정시각": "센서 시계열(시간축)",
    "배치": "공정조건",
    "온도": "센서 시계열",
    "OP값": "센서 시계열",
    "CP값": "센서 시계열",
    "상태": "품질 상태 라벨",
}
for i in range(len(header)):
    kinds = set(row[i] for row in rows)
    print(f"{header[i]:<6} 종류 {len(kinds):>3}가지 {roles[header[i]]}")


# ========================================================================
# 5. 눈으로 보면 모르는 것이, 재면 보입니다.
# ========================================================================
print("=" * 60)
print("[5] 온도 44개 전부")
print(temps)

avg = sum(temps) / len(temps)
top = max(temps)
low = min(temps)
span = top - low

print()
print("[5-1] 세 숫자로 44개를 요약")
print("합계:", round(sum(temps), 1), " / 개수:", len(temps))
print("평균:", round(avg, 2))
print("최대:", top, " / 최소:", low, " / 범위:", round(span, 1))

# 질문
# 온도가 평균에서 보통 몇도쯤 벗어나나?
# 재는 방법은 질문을 그대로 코드로 옮기면 됩니다.
# 1) 줄마다 평균에서 얼마나 떨어졌는지 계산한다
# 2) 위로 떨어진 것과 아래로 떨어진 것이 섞이면 더할 때 상쇄되니 부호를 없앤다
# 3) 그 거리들의 평균을 낸다
gaps = [abs(t - avg) for t in temps]
spread = sum(gaps) / len(gaps)
print()
print("[5-2] 흩어진 정도")
print("평균에서 떨어진 거리 중 가장 먼 것:", round(max(gaps), 2))
print("평균에서 떨어진 거리의 평균:", round(spread, 2))


# ========================================================================
# 6. 나눠서 재면 더 보입니다 - 배치별 비교
# ========================================================================
def stat(values):
    """
    숫자 리스트를 받아 개수, 평균, 최대, 최소, 범위, 흔들림을 딕셔너리로 돌려줍니다.
    왜 딕셔너리로 돌려주나 - 값 여섯 개를 튜플로 돌려주면 받는쪽에서 순서를 기억해야 합니다.
    """
    result = {
        "개수": len(values),
        "평균": round(sum(values) / len(values), 2),
        "최대": max(values),
        "최소": min(values),
        "범위": round(max(values) - min(values), 2),
    }
    gaps = [abs(v - result["평균"]) for v in values]
    result["흔들림"] = round(sum(gaps) / len(gaps), 2)
    return result


print("=" * 60)
print("[6] 배치별로 온도를 재 봅니다")
lots = ("로트A", "로트B", "로트C")  # 돌릴 배치 이름
for lot in lots:
    picked = []
    for row in rows:
        if row[1] == lot:
            picked.append(row)

    lot_temps = []
    for row in picked:
        lot_temps.append(float(row[2]))

    s = stat(lot_temps)
    print(lot, s)

print("전체", stat(temps))

# 검산 - 배치별 행 수의 합이 전체와 같아야 합니다
print()
print("[6-1] 검산 - 배치 이름을 하나 잘못 적으면")
for lot in ("로트A", "로트B", "로트c"):
    print(lot, len([row for row in rows if row[1] == lot]))

# 위에서 미리 적어둔 온도, OP, CP을 여기서 확인
print()
print("[6-2] 숫자 열 셋의 흔들림")
for name, idx in (("온도", 2), ("OP값", 3), ("CP값", 4)):
    print(name, "흔들림:", stat([float(row[idx]) for row in rows])["흔들림"])


# ========================================================================
# 7. 라벨 없이 수상한 줄 찾기
# ========================================================================
# 평균에서 흔들림의 몇 배보다 멀면 수상하다
print()
print("[7] 라벨을 보지않고 찾아낸 수상한 줄")
for k in (2, 3):
    far = [row for row in rows if abs(float(row[2]) - avg) > k * spread]
    print(f"흔들림 {k}배 초과: {len(far)}건")

    for row in far:
        print(
            f"{row[1]} {row[0]} 온도 {row[2]:>6}"
            f" 평균과 차이 {round(float(row[2]) - avg, 2):>6} 상태={row[5]}"
        )

"""
3배 차이 나는거에 분명 문제가 있는 친구가 있는데 이걸 적은 사람이 정상이라고 적었습니다.
1) 우리 기준이 빡빡해서 멀쩡한 줄을 잡은 것 (오탐)
2) 라벨이 빠뜨린 진짜 이상인데 사람이 못 보고 지나간 것
3) 정상의 정의가 우리 생각과 다른 것
어느 쪽인지 데이터만으로는 알 수 없습니다.
이 데이터에 설명 문서가 없어서 정상의 정의를 확인할 수 없음
현장에 물어봐야됨 - 이 시각에 무슨 일이 있었나요?
분석가가 데이터만 보고 결론을 내리면 안되는 이유가 이겁니다.
추측을 사실처럼 적는 순간 보고서 전체를 못 믿게 됩니다.
모르는 건 모른다고 적고 물어봅니다.
"""

# ========================================================================
# 8. 두 열이 같이 움직입니다 - 온도와 OP값
# ========================================================================
# 숫자를 재는 이유가 하나 더 있습니다. "두 칸이 서로 관계가 있나"를 볼 수 있어요
# 어려운 계산 없이 평균 비교만으로 보여 줄 수 있습니다.
# 온도가 높은 5줄과 낮은 5줄을 뽑아서 그때 OP값이 얼마였는지 비교합니다
pairs = sorted(((float(row[2]), float(row[3])) for row in rows), reverse=True)
hot = pairs[:5]
cold = pairs[-5:]
print("=" * 60)
print("[8] 온도가 높을때와 낮을때의 OP값")
print("온도 상위 5줄:", hot)
print("그때 OP값 평균:", round(sum(p[1] for p in hot) / 5, 1))
print("온도 하위 5줄:", cold)
print("그때 OP값 평균:", round(sum(p[1] for p in cold) / 5, 1))

# ========================================================================
# 9. 여기서 막힙니다. 열이 늘어나면 줄 수를 세봅니다
# ========================================================================
cols = {"온도": 2, "OP값": 3, "CP값": 4}
print(f"{'배치':<5}{'열':<6}{'개수':>5}{'평균':>10}{'최대':>10}{'최소':>10}")
for lot in ("로트A", "로트B", "로트C"):
    for name, idx in cols.items():
        vals = []
        for row in rows:
            if row[1] == lot and row[idx] != "":
                vals.append(float(row[idx]))
        print(
            f"{lot:<5}{name:<6}{len(vals):>5}{round(sum(vals) / len(vals), 2):>10}{max(vals):>10}{min(vals):>10}"
        )

# ========================================================================
# 10. 여기서 막힙니다. 빈칸이 섞이면 터뜨려 봅니다
# ========================================================================
with open(PROC, encoding="utf-8-sig") as f:
    r = csv.reader(f)
    dirty_header = next(r)
    dirty_rows = list(r)

print("=" * 60)
print("[10] 빈 칸이 섞인 파일")
print("행 수:", len(dirty_rows), " / 열 수:", len(dirty_header))
print("열 이름:", dirty_header)

for i in range(len(dirty_header)):
    blank = 0
    for row in dirty_rows:
        if row[i] == "":
            blank += 1
    if blank > 0:
        print(f"빈 칸 {blank:>2}개 - {dirty_header[i]}")

print()
print("[10-1] 방어 없이 평균을 내면")
try:
    op = [float(row[4]) for row in dirty_rows]
    print("평균", sum(op) / len(op))
except ValueError as e:
    print("ValueError:", e)

# ========================================================================
# 11. 그래서 다음 시간에 Numpy Pandas를 배웁니다
# ========================================================================

"""
데이터분석은 어디서나 같은 순서로 갑니다. 이 여섯 카은 외워 두세요.
  수집   ->   전처리    ->    EDA      ->  모델링   ->  평가  ->   현장적용
(모으고)     (청소하고)    (눈으로 보고)      (예측)     (검증)      (운영)
수집 : 센서 MES(생산관리시스템) 품질검사 결과를 모아옵니다.
전처리 : 결측치, 이상치, 단위를 정리합니다.
EDA(Exploratory Data Analysis) : 그래프와 통계로 데이터를 눈으로 이해합니다.
모델링 : 예측하는 규칙을 데이터에서 만들어 냅니다.
평가 : 그 규칙이 쓸만한지 재 봅니다.
현장적용 : 실제 공장에 걸어 두고 돌립니다. 여기서 또 문제가 나와 처음으로 돌아갑니다.
"""
