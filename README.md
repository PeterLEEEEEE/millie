# 📒 밀리의 서재 모티브의 전자책 구독 플랫폼 프로젝트 소개<br>
### 📍 프로젝트 개요 

독서와 무제한 친해지리, 전자책 구독서비스 밀리의 서재 어플리케이션을 모티브로 한 전자책 구독 플랫폼 구현 

<br>

### 📍 개발 인원과 기간<br>
##### ✅  개발팀
- 내일채움공책팀<br>
##### ✅  개발기간
- 2021/09/13 ~ 2021/10/1 (연휴기간 제외)<br>
##### ✅  개발 인원(총 6명)
- FE: 강연옥 조성환 주철진 (3명)<br>
- BE: 박지원 신우주 이무현 (3명)<br>

##### ❗️ Reference
이 프로젝트는 밀리의 서재 어플리케이션을 참조하여 학습목적으로 만들었습니다.
실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.


<div id=header align="center">
  <a href="https://www.youtube.com/watch?v=WJS8kuzjzJU">👉🏻 시연 영상 보러가기</a>
</div>

<br>
<br>

### 📍 프로젝트 소개
'밀리의 서재' 어플리케이션을 벤치마킹하여 전자책 구독 플랫폼 서비스를 구축했습니다. <br>
애자일 방법론을 채택하여 연휴를 제외하고 총 2주 간 스프린트 방식으로 프로젝트를 진행했습니다. 사용자에게 편리하고 유용한 서비스를 제공할 수 있는 방법을 고민하고 실행에 옮기는 것을 기초 목적으로 삼았으며, 효율적인 아키텍처 구축을 위해 노력했습니다. <br><br>
백엔드팀에서는 사용자 중심의 다양한 서비스를 제공하기 위해 효율적인 데이터 모델링 방안을 고민했습니다. 최적화된 데이터베이스 사용을 목적으로 장고 ORM을 사용하였고, AWS의 RDS, EC2, S3버킷 등을 사용하여 시스템 아키텍쳐를 설계했습니다. 각 기능에 대해 유닛테스트를 진행하여 여러 환경 변수에 대한 안정성을 확보했습니다. <br><br>
프론트엔드팀에서는 React Hooks와 Styled-Component, 라이브러리 등을 이용하여 사용자의 흥미를 이끌어낼 수 있는 UI/UX를 구현했습니다. 직관적인 구조 파악과 재사용성을 염두에 두고 컴포넌트를 분리시켰으며, 동시에 API 통신으로 받은 데이터의 효율적 전달성을 확보했습니다.<br><br>



## 📅 Plan
✅ 프로젝트 수행 기간<br>
  2021.09.13 ~ 2021.10.1 (연휴기간 제외)

✅ 프로젝트 수행 방법
  애자일 방법론을 활용한 스크럼 방식 

<table style="text-align:center; margin:auto;">
  <tr>
    <th colspan="4" style="font-size:20px">1주차</th>
  </tr>
  <tr>
    <td colspan="4">
      <ul style="text-align:left">
        <li> FE - 소셜로그인, 메인페이지, 검색창 페이지 구현</li>
        <li> BE - 소셜로그인 통신확인, 데이터 모델링, 각 페이지 로직 구현</li>
      </ul>
    </td>
  </tr>
  <tr>
    <th colspan="4" style="font-size:20px">2주차</th>
  </tr>
  <tr>
    <td colspan="4">
      <ul style="text-align:left">
        <li> FE - 상세페이지, Nav & Footer, 뷰어 기능 등 구현, 동적 라우팅 구성 및 구동 확인</li>
        <li> BE - 배포 및 유닛테스트 </li>
      </ul>
    </td>
  </tr>
  </table>

<br>

## 📕 Teammate

<div id=teammate>
  <h4> 🎨 Front-End </h4>
  <table style="text-align:center;">
    <tr>
      <th><a href="https://github.com/janine-kang">강연옥</a></th>
      <th><a href="https://github.com/choseonghwan91">조성환</a></th>
      <th><a href="https://github.com/JUCHEOLJIN">주철진</a></th>
    </tr>
    <tr>
      <td>
       * 검색창 구현<br>
         - 카테고리별 검색<br>
         - 필터링 기능<br>
         - 검색결과 페이지<br>
       * 뷰어 기능 구현<br>
         - 한 쪽 보기/두 쪽 보기<br>
         - 목차기능<br>
         - 페이지 이동 기능<br>
      </td>
      <td>
       * Nav바 구현<br>
       * 소셜로그인 페이지 구현(Kakao)<br>
       * 나의 서재 페이지 구현<br>
         - 전체도서보기<br>
         - 나의 책장 보기<br>
      </td>
      <td>
       * 메인페이지 구현<br>
         - Carousel<br>
         - 도서 추천서비스<br>
         - 오늘의 도서 보기<br>
       * 상세페이지 구현<br>
         - 책 정보 보기<br>
         - 바로 읽기 기능<br>
         - 댓글 및 좋아요 기능<br>
         - 내 서재에 책 담기 기능<br>
         - 책장 추가 기능<br>
       * Footer 구현<br>
      </td>
    </tr>
  </table>
  <br>
  <h4> 🛢 Back-End </h4>
  <table style="text-align:center;">
    <tr>
      <th><a href="https://github.com/jiwon5304">박지원</a></th>
      <th><a href="https://github.com/shinwooju">신우주</a></th>
      <th><a href="https://github.com/PeterLEEEEEE">이무현</a></th>
    </tr>
    <tr>
      <td>
       * DB 모델링<br>
       * 나의 서재와 책장기능 로직 구현<br>
       * HTTP Methods 이용한 엔드포인트 구현 <br>
      </td>
      <td>
       * DB 모델링<br>
       * 소셜로그인(kakao)<br>
       * 데코레이터<br>
       * 뷰어기능 로직 구현, HTTP Methods 이용한 엔드포인트 구현 
      </td>
      <td>
       * DB 모델링<br>
       * 메인페이지와 상세페이지 로직 구현<br>
       * AWS 배포: RDS,S3 업로드, EC2 배포
      </td>
    </tr>       
  </table>
  <br>
  
</div>

