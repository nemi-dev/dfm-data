# 던전앤파이터 모바일 아이템 모음

던파모바일에 나오는 아이템들을 모으고 있는 저장소입니다.  
[vscode](https://code.visualstudio.com/)에서 작업하기에 최적화되어 있습니다.  


- [던전앤파이터 모바일 아이템 모음](#던전앤파이터-모바일-아이템-모음)
- [파일 구성](#파일-구성)
  - [공통](#공통)
  - [베이스 아이템 (/data/baseitem)](#베이스-아이템-databaseitem)
  - [아이템 (/data/item)](#아이템-dataitem)
  - [세트 (/data/itemset)](#세트-dataitemset)
  - [패시브/버프 스킬 (/data/selfskill)](#패시브버프-스킬-dataselfskill)
  - [공격 스킬 (/data/skill)](#공격-스킬-dataskill)
  - [직업 (/data/dfclass)](#직업-datadfclass)
- [효과](#효과)


# 파일 구성

## 공통

- 기본적으로 [JSON](https://www.json.org/)을 사용해 데이터를 작성합니다만, [YAML](https://yaml.org)을 도입할 의향도 있습니다.
- /data 폴더의 한 단계 하위 폴더부터는 경로명은 고려하지 않고, 오로지 파일명으로만 데이터를 구분합니다. 폴더는 파일을 분류하기 위한 수단일 뿐입니다.
  > 예를 들어, '/data/item/**오즈마장비.json**' 과 '/data/item/레이드/**오즈마장비.json**' 은 서로 같은 것으로 취급해서 둘이 동시에 존재하면 안되지만, '/data/item/**오즈마장비.json**'과 '/data/itemset/**오즈마장비.json**'은 다른 것으로 취급합니다.
- 어떤 `*.json` 파일에는 `id`값이 있습니다. 이것은 (아직은) 사용자가 직접 설정하지 않아도 됩니다.

## 베이스 아이템 (/data/baseitem)

아무런 부가효과가 없는 특정 등급, 특정 재질, 특정 종류의 베이스 아이템입니다.

무기, 팔찌, 목걸이, 반지, 보조장비는 여기 있는 베이스 아이템들의 효과를 그대로 가져다 만들어도 됩니다.

방어구는 던파모바일 스탯계산기에서 사용자가 지정한 방어구 재질 또는 아이템 자신이 직접 고정시킨 방어구 재질을 자동으로 결합하므로, 아이템을 만들 때 이 폴더에 있는 베이스 아이템 효과들을 추가하지 말아야 합니다.

## 아이템 (/data/item)

던파모바일에서 볼 수 있는 아이템들을 나타냅니다.

> 베이스 아이템 문단에서 설명한 대로 방어구를 만들 때에는 방어구 기본옵을 제외한 옵션들만 추가해야 합니다.

취급하는 아이템 종류는 다음과 같습니다.

- 무기
- 방어구: 상의, 하의, 머리어깨, 벨트, 신발
- 악세서리: 팔찌, 목걸이, 반지
- 보조장비
- 성안의 봉인: 봉인석, 정수
- 칭호
- 오라
- 무기아바타
- 크리쳐 (레어 이상)
- 아티팩트 (레어 이상)
- 카드 + 보주 (레어 이상, 현재는 효과가 같은 것은 어느 하나만 취급중)
- 할기의 본링
- 블랙 펄: 미스트

취급하는 아이템 컨텐츠는 다음과 같습니다.

- 서부 지옥파티 (60에픽)
- 환영극단 2막 (에픽만, **🛠️현재 작업중!!**)
- 솔라리스 악세서리
- 솔라리스의 대양 무기 (60제)
- 혼돈의 개막 + 혼돈의 종막
- 강림:오즈마 보조장비

**취급하지 않는** 아이템은 다음과 같습니다. (이들은 다른 방법으로 구현됩니다.)

- 엠블렘
- 마법봉인
- 의상 아바타
- 강화 보너스, 마력결정, 길드 버프

## 세트 (/data/itemset)

세트 아이템들을 장착했을 때 나타나는 "세트"를 나타냅니다.

1. 세트를 먼저 정의합니다. 세트는 이렇게 생겼습니다.
    ````json
    {
      "name": "<세트 이름>",
      "<세트 아이템 수>": {
        // 해당 수만큼 모으면 활성화되는 세트 효과
      },
      // ...
    }
    ````
    예를 들어, **스테이시의 암살복** 세트는 이렇게 구성됩니다.

    ````json
    {
      "name": "스테이시의 암살복", 
      "2": { // 암살 2세트를 착용하면
        "name": "스테이시의 암살복[2]", 
        "attrs": {
          "sk_inc": 13 // 스킬 공격력 증가 +13% 적용
        }
      }, 
      "5": { // 암살 5세트를 착용하면
        "name": "스테이시의 암살복[5]", 
        "attrs": {
          "dmg_inc": 8,  // 데미지 증가 +8% 적용
          "cdmg_inc": 40 // 크리티컬 데미지 증가 +40% 적용
        }
      }
    }
    ````
    
    > "스테이시의 암살복\[2]" 처럼 숫자가 붙은 이름은 어떤 버그를 해결하려던 흔적으로, 이후에 제거될 수 있습니다.

2. 각 아이템 파일 (`/data/item/**/*.json`)의 `setOf` 속성에다 세트 이름을 지정합니다.
    ````json
    {
      // ... 기본 정보
      "setOf": ["<세트 이름>"],
      // ... 다른 정보
    }
    ````

## 패시브/버프 스킬 (/data/selfskill)

`/data/selfskill/**/*.json`은 이렇게 생겼습니다.

````json
{
  "name": "<스킬이름>",
  "acquire": {
    // 스킬을 찍기만 해도 적용되는 효과
    // (ex. 마도학자의 "스위트 캔디바"는 버프지만 찍기만 해도 지능을 올려준다)
  },
  "acquireGives": {
    // 스킬을 찍기만 해도 파티원 모두에게 적용되는 효과
    // (이런 게 던파모바일에 아직은 없는 걸로 알고 있음)
  },
  "dungeon": {
    // 스킬을 찍기만 해도 던전 입장 시 자신에게 적용되는 효과
  },
  "buff": {
    // (버프일 때만) 스킬 사용시 자신에게 적용되는 효과
  },
  "buffGives": {
    // (버프일 때만) 스킬 사용시 파티원 모두에게 적용되는 효과
  }
}
````

예를 들어, "고대의 도서관.json"은 이렇게 생겼습니다.

````json
{
  "name": "고대의 도서관",
  "acquire": { // 이 스킬을 찍었을 때,
    "DefBreak": { // "적의 방어력 퍼센트 감소" 효과를 적용한다.
      "base": 2.8, "inc": 0.2571 // ( 2.8 + 0.2571 × <스킬레벨> )% 만큼
    }
  }
}
````

## 공격 스킬 (/data/skill)

공격 스킬들을 나타냅니다. 대략 이렇게 생겼습니다.

````json
{
  "name": "메가 드릴(대성공)", // 스킬 이름
  "level": 45,
  "point": 55,
  "cool": 40,
  "eltype": ["Ice"],
  "attacks": [ // 메가 드릴 1회 사용 시
     // 꺼낼 때 ( 1029.75 + 116.25 × <스킬레벨> )% 데미지를 줌
    {
      "atName": "꺼내기", 
      "value": {
        "base": 1029.75,
        "inc": 116.25
      }
    },
    // 드릴로 ( 179.6666 + 20.3334 × <스킬레벨> )%만큼 최대 42회 타격
    {
      "atName": "타격",
      "value": {
        "base": 179.6666,
        "inc": 20.3334
      },
      "maxHit": 42
    },
    // 터질 때 ( 1544.5833 + 174.4167 × <스킬레벨> )% 데미지를 줌
    {
      "atName": "폭발",
      "value": {
        "base": 1544.5833,
        "inc": 174.4167
      }
    }
  ]
}
````


## 직업 (/data/dfclass)

던파모바일 직업을 나타냅니다. 여기에 각 직업의 고유 공격타입, 속성공격, 고유 효과, 사용가능한 스킬 등이 작성됩니다.

# 효과

아이템을 착용했을 때, 특정 스킬을 썼을 때 적용되는 효과 모델입니다.

| 키 | 설명 | 타입 | 단위 |
| --- | --- | --- | --- |
| `strn` | 힘 | number |   |
| `intl` | 지능 | number |   |
| `str_inc` | 힘 증가 | number | %  |
| `int_inc` | 지능 증가 | number | %  |
| `atk_ph` | 물리 공격력 | number |   |
| `atk_mg` | 마법 공격력 | number |   |
| `atk_ph_inc` | 물리 공격력 증가 | number | %  |
| `atk_mg_inc` | 마법 공격력 증가 | number | %  |
| `crit_ph` | 물리 크리티컬 | number |   |
| `crit_mg` | 마법 크리티컬 | number |   |
| `crit_ph_pct` | 물리 크리티컬 확률 증가 | number | %  |
| `crit_mg_pct` | 마법 크리티컬 확률 증가 | number | %  |
| `dmg_inc` | 데미지 증가 | number | %  |
| `cdmg_inc` | 크리티컬 데미지 증가 | number | %  |
| `catk_inc` | 크리티컬 공격력 증가 (버서커/이단심판관 등) | number | % |
| `dmg_add` | 추가 데미지 | number | %  |
| `eltype` | 속성 부여 | array |   |
| `el_fire` | 화속성 강화 | number |   |
| `el_ice` | 수속성 강화 | number |   |
| `el_lght` | 명속성 강화 | number |   |
| `el_dark` | 암속성 강화 | number |   |
| `DualTrigger` | 화속성강화와 명속성강화를 높은 쪽으로 같게 함 | boolean |   |
| `eldmg_fire` | 화속성 추가 데미지 | number | %  |
| `eldmg_ice` | 수속성 추가 데미지 | number | %  |
| `eldmg_lght` | 명속성 추가 데미지 | number | %  |
| `eldmg_dark` | 암속성 추가 데미지 | number | %  |
| `AddMaxEldmg` | 속성강화가 가장 높은 속성 추가 데미지 | number | %  |
| `sk_inc` | 스킬 공격력 증가 | number | %  |
| `sk_inc_sum` | 단리 적용되는 (ex. 패시브 스킬) 스킬 공격력 증가 | number | %  |
| `sk_lv` | 특정 스킬 레벨 증가 | { \[스킬이름]: number } |   |
| `sk_val` | 특정 공격스킬의 일부 또는 모든 계수 증가 | { \[스킬이름]: number } | %  |
| `skb_add` | 특정 스킬의 버프 수치 증가 | { \[스킬이름]: number } |   |
| `sk_hit` | 특정 공격스킬의 일부 타격횟수 증가 | { \[스킬이름]: number } |   |
| `sk_dur` | 특정 스킬 지속시간 증가 | { \[스킬이름]: number } |   |
| `sk_cool` | 특정 스킬 쿨타임 증가/감소 | { \[스킬이름]: number } | %  |
| `target_def` | 적 방어력 변화 (ex.로딘글로) | number |   |
| `target_res` | 적 속성저항 변화 (모든속성) | number |   |
| `DefBreak` | 적 방어력 퍼센트 감소 | number | %  |
| `speed_atk` | 공격 속도 증가 | number | %  |
| `speed_cast` | 캐스팅 속도 증가 | number | %  |
| `speed_move` | 이동 속도 증가 | number | %  |
| `Accu` | 적중 | number |   |
| `AccuPct` | 적중 확률 증가 | number | %  |
| `hpmax` | HP MAX (실적용 제외) | number |   |
| `mpmax` | MP MAX (실적용 제외) | number |   |
| `vit` | 체력 | number |   |
| `psi` | 정신력 | number |   |
| `def_ph` | 물리 방어력 | number |   |
| `def_mg` | 마법 방어력 | number |   |
| `def_ph_pct` | 물리 방어력 증가 | number | %  |
| `def_mg_pct` | 마법 방어력 증가 | number | %  |
| `res_fire` | 화속성 저항 | number |   |
| `res_ice` | 수속성 저항 | number |   |
| `res_lght` | 명속성 저항 | number |   |
| `res_dark` | 암속성 저항 | number |   |
| `Evd` | 회피 | number |   |
| `EvPct` | 회피 확률 증가 | number | % |
| `Walk` | 마을 이동속도 증가 | number | % |
| `maxRepeat` | 최대 중첩 횟수 | number |   |
