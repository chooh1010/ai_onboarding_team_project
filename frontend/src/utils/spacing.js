export function applySpacing(text) {
  if (!text || typeof text !== 'string') return text;
  let s = text.trim();

  // 여러 공백을 하나로
  s = s.replace(/\s+/g, ' ');

  // 한글 <-> 영문/숫자 사이 공백 추가
  s = s.replace(/([\uAC00-\uD7A3])([A-Za-z0-9])/g, '$1 $2');
  s = s.replace(/([A-Za-z0-9])([\uAC00-\uD7A3])/g, '$1 $2');

  // 괄호/구두점 앞 불필요한 공백 제거
  s = s.replace(/\s+([.,?!:;…)\]])/g, '$1');

  // 쉼표 뒤 한 칸 확보
  s = s.replace(/,([^\s])/g, ', $1');

  // 앞뒤 공백 정리
  return s.trim();
}