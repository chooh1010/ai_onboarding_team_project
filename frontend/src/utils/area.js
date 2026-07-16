const AREA_NAMES = {
  '5': {
    default: '광주',
    '1': '광주 광산구',
    '2': '광주 남구',
    '3': '광주 동구',
    '4': '광주 북구',
    '5': '광주 서구',
  },
  '37': {
    default: '전북',
    '4': '남원',
    '12': '전주',
  },
  '38': {
    default: '전남',
    '6': '나주',
    '7': '담양',
    '11': '순천',
    '13': '여수',
    '19': '장성',
    '21': '진도',
    '23': '해남',
    '24': '화순',
  },
}

export function getAreaLabel(areaCode, sigunguCode, address = '') {
  const group = AREA_NAMES[String(areaCode || '')]
  const label = group?.[String(sigunguCode || '')] || group?.default
  if (label) return label

  const normalized = String(address || '').trim()
  if (!normalized) return '전라남도'

  const match = normalized.match(/(광주|전주|여수|담양|나주|화순|장성|해남|진도|순천|남원)[^\s]*/)
  return match?.[0] || '전라남도'
}
