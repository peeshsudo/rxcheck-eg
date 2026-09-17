-- Minimal seed for local development
INSERT INTO drugs (rxcui, generic_en, generic_ar, drug_class) VALUES
  ('32968', 'clopidogrel',   'كلوبيدوجريل',   'Antiplatelet'),
  ('7646',  'omeprazole',    'أوميبرازول',    'PPI'),
  ('11289', 'warfarin',      'وارفارين',      'Anticoagulant'),
  ('1191',  'aspirin',       'أسبرين',        'NSAID / antiplatelet'),
  ('41493', 'metformin',     'ميتفورمين',     'Antidiabetic'),
  ('6809',  'levothyroxine', 'ليفوثيروكسين',  'Thyroid hormone');

INSERT INTO products (drug_id, brand_en, brand_ar, market, registration_no, source) VALUES
  ((SELECT id FROM drugs WHERE generic_en='clopidogrel'), 'Plavix', 'بلافيكس', 'EG', 'EDA-001', 'EDA'),
  ((SELECT id FROM drugs WHERE generic_en='omeprazole'),  'Losec',  'لوسيك',  'EG', 'EDA-002', 'EDA'),
  ((SELECT id FROM drugs WHERE generic_en='warfarin'),    'Marevan','ماريفان','EG', 'EDA-003', 'EDA');