export const EXHIBIT_TEMPLATE_HEADERS = ['展品名称', '时间', '地点', '材质', '介绍', '图片', '其他'];

export function getExhibitName(exhibit) {
  return exhibit?.name || exhibit?.['展品名称'] || exhibit?.名称 || exhibit?.品名 || '';
}

export function getExhibitTime(exhibit) {
  return exhibit?.time || exhibit?.era || exhibit?.['时间'] || exhibit?.年代 || exhibit?.时代 || '';
}

export function getExhibitPlace(exhibit) {
  return exhibit?.place || exhibit?.['地点'] || exhibit?.origin || exhibit?.出土地 || exhibit?.产地 || exhibit?.来源 || '';
}

export function getExhibitMaterial(exhibit) {
  return exhibit?.material || exhibit?.mat || exhibit?.['材质'] || '';
}

export function getExhibitIntroduction(exhibit) {
  return exhibit?.introduction || exhibit?.description || exhibit?.['介绍'] || exhibit?.描述 || exhibit?.简介 || '';
}

export function getExhibitImage(exhibit) {
  return exhibit?.thumbnail_url || exhibit?.image_url || exhibit?.image || exhibit?.['图片'] || '';
}

export function getExhibitOther(exhibit) {
  return exhibit?.other || exhibit?.size || exhibit?.sz || exhibit?.['其他'] || exhibit?.尺寸 || '';
}

export function normalizeImportedExhibit(exhibit = {}) {
  const name = String(getExhibitName(exhibit) || '').trim();
  const time = String(getExhibitTime(exhibit) || '').trim();
  const place = String(getExhibitPlace(exhibit) || '').trim();
  const material = String(getExhibitMaterial(exhibit) || '').trim();
  const introduction = String(getExhibitIntroduction(exhibit) || '').trim();
  const imageUrl = String(exhibit?.image_url || exhibit?.image || exhibit?.['图片'] || '').trim();
  const thumbnailUrl = String(exhibit?.thumbnail_url || imageUrl).trim();
  const other = String(getExhibitOther(exhibit) || '').trim();

  return {
    ...exhibit,
    name,
    time,
    place,
    material,
    introduction,
    image_url: imageUrl,
    thumbnail_url: thumbnailUrl,
    other,
    // 兼容项目里仍有部分旧逻辑读取旧字段名
    era: time,
    description: introduction,
    size: other,
  };
}

export function hasMeaningfulExhibitData(exhibit = {}) {
  return [
    getExhibitName(exhibit),
    getExhibitTime(exhibit),
    getExhibitPlace(exhibit),
    getExhibitMaterial(exhibit),
    getExhibitIntroduction(exhibit),
    getExhibitImage(exhibit),
    getExhibitOther(exhibit),
  ].some((value) => String(value || '').trim() !== '');
}

export function getIncompleteExhibitFields(exhibit = {}) {
  const mapping = [
    ['展品名称', getExhibitName(exhibit)],
    ['时间', getExhibitTime(exhibit)],
    ['地点', getExhibitPlace(exhibit)],
    ['材质', getExhibitMaterial(exhibit)],
    ['介绍', getExhibitIntroduction(exhibit)],
    ['图片', getExhibitImage(exhibit)],
    ['其他', getExhibitOther(exhibit)],
  ];

  return mapping
    .filter(([, value]) => String(value || '').trim() === '')
    .map(([label]) => label);
}

export function isIncompleteExhibit(exhibit = {}) {
  return hasMeaningfulExhibitData(exhibit) && getIncompleteExhibitFields(exhibit).length > 0;
}
