import streamlit as st
import yfinance as yf
import math

st.title("ETF 선택 및 매수금액/비중 계산기")

# =============================================================================
# 1. ETF 그룹 정보 정의
# =============================================================================
# 국내 ETF 그룹 (연금계좌용; 티커에 .KS 붙임)
domestic_groups = {
    "한국주식추종": {
        "069500.KS": "KODEX 200(069500)",
        "229200.KS": "KODEX 코스닥150(229200)",
        "102780.KS": "KODEX 삼성그룹(102780)",
        "305720.KS": "KODEX 2차전지산업(305720)",
        "466920.KS": "SOL 조선TOP3플러스(466920)",
        "396500.KS": "TIGER Fn반도체TOP10(396500)",
        "161510.KS": "PLUS 고배당주(161510)",
        "466940.KS": "TIGER 은행고배당플러스TOP10(466940)",  
        "228790.KS": "TIGER 화장품(228790)",
        "091180.KS": "KODEX 자동차(091180)"
    },
    "국채/채권": {
        "459580.KS": "KODEX CD금리액티브(459580)",
        "385560.KS": "RISE KIS국고채30년Enhanced(385560)",
        "439870.KS": "KODEX 국고채30년액티브(439870)",
        "148070.KS": "KIWOOM 국고채10년(148070)",
        "114260.KS": "KODEX 국고채3년(114260)",
        "453850.KS": "ACE 미국30년국채액티브(H)(453850)",
        "449170.KS": "TIGER KOFR금리액티브(합성)(449170)",
        "447770.KS": "TIGER 테슬라채권혼합Fn(447770)",
        "448540.KS": "ACE 엔비디아채권혼합블룸버그(448540)",
        "438080.KS": "ACE 미국S&P500채권혼합액티브(438080)",
        "475080.KS": "KODEX 테슬라커버드콜채권혼합액티브(475080)",
        "472170.KS": "TIGER 미국테크TOP10채권혼합(472170)",
        "329650.KS": "KODEX TRF3070(329650)",
        "438100.KS": "ACE 미국나스닥100채권혼합액티브(438100)"
    },
    "안전자산(금)": {
        "411060.KS": "ACE KRX금현물(411060)",
        "329200.KS": "TIGER 리츠부동산인프라(329200)",
        "476800.KS": "KODEX 한국부동산리츠인프라(476800)"
    },
    "해외주식형": {
        "360750.KS": "TIGER 미국S&P500(360750)",
        "379800.KS": "KODEX 미국S&P500(379800)",
        "360200.KS": "ACE 미국S&P500(360200)",
        "133690.KS": "TIGER 미국나스닥100(133690)",
        "379810.KS": "KODEX 미국나스닥100(379810)",
        "367380.KS": "ACE 미국나스닥100(367380)",
        "489250.KS": "KODEX 미국배당다우존스(489250)",
        "458730.KS": "TIGER 미국배당다우존스(458730)",
        "446720.KS": "SOL 미국배당다우존스(446720)",
        "381180.KS": "TIGER 미국필라델피아반도체나스닥(381180)",
        "446770.KS": "ACE 글로벌반도체TOP4 Plus SOLACTIVE(446770)",
        "381170.KS": "TIGER 미국테크TOP10 INDXX(381170)",
        "314250.KS": "KODEX 미국빅테크10(H)(314250)",
        "465580.KS": "ACE 미국빅테크TOP7 Plus(465580)",
        "457480.KS": "ACE 테슬라밸류체인액티브(457480)",
        "487230.KS": "KODEX 미국AI전력핵심인프라(487230)",
        "481180.KS": "SOL 미국AI소프트웨어(481180)",
        "456600.KS": "TIMEFOLIO 글로벌AI인공지능액티브(456600",
        "473460.KS": "KODEX 미국서학개미(473460)",
        "458760.KS": "TIGER 미국배당다우존스타겟커버드콜2호(458760)",
        "486290.KS": "TIGER 미국나스닥100타겟데일리커버드콜(486290)",
        "474220.KS": "TIGER 미국테크TOP10타겟커버드콜(474220)",
        "251350.KS": "KODEX 선진국MSCI World(251350)",
        "488500.KS": "TIGER 미국S&P500동일가중(488500)"
    },
    "신흥국주식": {
        "371460.KS": "TIGER 차이나전기차SOLACTIVE(371460)",
        "453870.KS": "TIGER 인도니프티50(453870)",
        "371160.KS": "TIGER 차이나항셍테크(371160)",
        "241180.KS": "TIGER 일본니케이225(241180)",
        "245710.KS": "ACE 베트남VN30(합성)(245710)"
    }
}

# 해외 ETF 그룹 (직투계좌용, 대표 해외 ETF 약 30종)
overseas_groups = {
    "미국주식추종": {
         "VOO": "VOO (Vanguard S&P 500 ETF)",
         "SPY": "SPY (SPDR S&P 500 ETF Trust)",
         "SCHD": "SCHD (Schwab U.S. Dividend Equity ETF)",
         "QQQ": "QQQ (Invesco QQQ Trust)",
         "QQQM": "QQQM (Invesco NASDAQ 100 ETF)",
         "QLD": "QLD (2x NASDAQ 100 ETF)",
         "TQQQ": "TQQQ(3x NASDAQ 100 ETF)",
         "SOXX": "SOXX(iShares Semiconductor ETF)",
         "SOXL": "SOXL(Direxion Dly Semiconductor Bull 3X)"
    },
    "국채/채권": {
         "TLT": "TLT (iShares 20+ Yr Treasury)",
         "IEF": "IEF (iShares 7-10 Year Treasury Bond)",
         "HYG": "HYG (iShares iBoxx $ High Yield Corporate Bond ETF)"
    },
    "안전자산(금)": {
         "GLD": "GLD (SPDR Gold Shares)",
         "SLV": "SLV (iShares Silver Trust)"
    },
    "기타": {
         "EFA": "EFA (iShares MSCI EAFE ETF)",
         "EEM": "EEM (iShares MSCI Emerging Markets ETF)",
         "VNQ": "VNQ (Vanguard Real Estate ETF)",
         "USO": "USO (United States Oil Fund)",
         "DBC": "DBC (Invesco DB Commodity Index Tracking Fund)",
         "XLF": "XLF (Financial Select Sector SPDR Fund)",
         "XLK": "XLK (Technology Select Sector SPDR Fund)",
         "XLY": "XLY (Consumer Discretionary Select Sector SPDR Fund)",
         "XLP": "XLP (Consumer Staples Select Sector SPDR Fund)",
         "XLE": "XLE (Energy Select Sector SPDR Fund)",
         "XLV": "XLV (Health Care Select Sector SPDR Fund)",
         "XLI": "XLI (Industrial Select Sector SPDR Fund)",
         "XLB": "XLB (Materials Select Sector SPDR Fund)",
         "XLRE": "XLRE (Real Estate Select Sector SPDR Fund)"
    }
}

# =============================================================================
# 2. ETF 선택하기
# =============================================================================
account_type = st.selectbox("계좌 유형 선택", ["연금계좌 (국내)", "직투계좌 (해외)"])
if account_type == "연금계좌 (국내)":
    available_etfs = {}
    for group_name, etf_dict in domestic_groups.items():
        available_etfs.update(etf_dict)
else:
    available_etfs = {}
    for etf_dict in domestic_groups.values():
        available_etfs.update(etf_dict)
    for etf_dict in overseas_groups.values():
        available_etfs.update(etf_dict)

# available_etfs의 value(표시명) 리스트 만들기
etf_names = list(available_etfs.values())
selected_etf_names = st.multiselect("선택할 ETF를 고르세요", etf_names)

# '선택완료' 버튼을 누르면 선택한 ETF 목록을 세션에 저장
if st.button("선택완료"):
    st.session_state.selected_etf = selected_etf_names

# =============================================================================
# 3. 매수금액 및 투자 비중 입력 메뉴 (ETF 선택 후 표시)
# =============================================================================
if 'selected_etf' in st.session_state and st.session_state.selected_etf:
    st.subheader("매수금액 및 투자 비중 입력")
    # 총 매수금액 입력
    investment = st.number_input("총 매수금액 (원):", min_value=0, value=3000000, step=100000)
    st.write("### 선택한 ETF별 투자 비중 입력 (합계 100%가 되어야 함)")
    
    # 선택한 ETF별 투자 비중 입력 위젯 (정수형 입력, 소수점 없이)
    allocations = {}
    for etf in st.session_state.selected_etf:
        allocations[etf] = st.number_input(
            f"{etf} 비중 (%)", 
            min_value=0, max_value=100, value=0, step=1, format="%d", key=f"alloc_{etf}"
        )
    
    # "계산하기" 버튼을 눌렀을 때, 각 ETF별로 몇 주를 매수할 수 있는지 계산
    if st.button("계산하기"):
        total_alloc = sum(allocations.values())
        if total_alloc != 100:
            st.error(f"입력된 비중의 총합은 {total_alloc}% 입니다. 총합이 100%가 되어야 합니다.")
        else:
            st.subheader("매수 가능한 주 수 결과")
            # 역매핑: ETF 표시명 → 티커
            name_to_ticker = {v: k for k, v in available_etfs.items()}
            for etf in st.session_state.selected_etf:
                ticker = name_to_ticker.get(etf)
                # 각 ETF에 배정된 매수금액 계산
                allocated_amount = investment * (allocations[etf] / 100)
                try:
                    # yfinance를 통해 해당 티커의 최신 가격(종가) 조회
                    ticker_obj = yf.Ticker(ticker)
                    price_data = ticker_obj.history(period="1d")
                    if price_data.empty:
                        st.error(f"{etf} ({ticker})의 가격 데이터를 불러오지 못했습니다.")
                        continue
                    latest_price = price_data["Close"].iloc[-1]
                    # 배정금액으로 매수가 가능한 주 수 (내림)
                    share_count = math.floor(allocated_amount / latest_price)
                    st.write(f"ㅇ {etf} ({ticker}) : {share_count}주  (단위당 가격: {latest_price:,.0f} 원)")
                except Exception as e:
                    st.error(f"{etf} ({ticker})의 가격 정보를 불러오는 중 오류 발생: {e}")
