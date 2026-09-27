-- ============================================================
-- Expanded Egyptian seed — additional generics + brands
-- Idempotent. Safe to re-run.
-- ============================================================

-- -------- More generics --------
INSERT INTO drugs (rxcui, generic_en, generic_ar, drug_class) VALUES
  -- Cardiology
  (NULL, 'Ramipril',        'راميبريل',          'ACE inhibitor'),
  (NULL, 'Perindopril',     'بيريندوبريل',       'ACE inhibitor'),
  (NULL, 'Olmesartan',      'أولميسارتان',       'ARB'),
  (NULL, 'Telmisartan',     'تلميسارتان',        'ARB'),
  (NULL, 'Nebivolol',       'نيبيفولول',         'Beta-blocker'),
  (NULL, 'Ivabradine',      'إيفابرادين',        'Heart rate reducer'),
  (NULL, 'Amiodarone',      'أميودارون',         'Antiarrhythmic'),
  (NULL, 'Ticagrelor',      'تيكاجريلور',        'Antiplatelet'),
  (NULL, 'Prasugrel',       'براسوجريل',         'Antiplatelet'),
  (NULL, 'Ezetimibe',       'إيزيتيميب',         'Lipid-lowering'),
  (NULL, 'Fenofibrate',     'فينوفايبرات',       'Fibrate'),
  -- Diabetes
  (NULL, 'Dapagliflozin',   'داباجليفلوزين',     'SGLT2 inhibitor'),
  (NULL, 'Linagliptin',     'ليناجليبتين',       'DPP-4 inhibitor'),
  (NULL, 'Saxagliptin',     'ساكساجليبتين',      'DPP-4 inhibitor'),
  (NULL, 'Liraglutide',     'ليراجلوتايد',       'GLP-1 agonist'),
  (NULL, 'Insulin Aspart',  'إنسولين أسبارت',    'Antidiabetic'),
  (NULL, 'Insulin Detemir', 'إنسولين ديتمير',    'Antidiabetic'),
  (NULL, 'Pioglitazone',    'بيوجليتازون',       'Antidiabetic'),
  -- GI
  (NULL, 'Rabeprazole',     'رابيبرازول',        'PPI'),
  (NULL, 'Sucralfate',      'سكرالفات',          'Mucosal protectant'),
  (NULL, 'Mesalazine',      'ميسالازين',         'IBD drug'),
  (NULL, 'Ursodeoxycholic Acid','حمض الأورسوديوكسيكوليك', 'Bile acid'),
  -- Anti-infectives
  (NULL, 'Cefuroxime',      'سيفيوروكسيم',       'Antibiotic'),
  (NULL, 'Cefdinir',        'سيفدينير',          'Antibiotic'),
  (NULL, 'Ceftazidime',     'سيفتازيديم',        'Antibiotic'),
  (NULL, 'Meropenem',       'ميروبينيم',         'Antibiotic'),
  (NULL, 'Vancomycin',      'فانكوميسين',        'Antibiotic'),
  (NULL, 'Linezolid',       'لينيزوليد',         'Antibiotic'),
  (NULL, 'Fosfomycin',      'فوسفوميسين',        'Antibiotic'),
  (NULL, 'Oseltamivir',     'أوسيلتاميفير',      'Antiviral'),
  (NULL, 'Valacyclovir',    'فالاسيكلوفير',      'Antiviral'),
  (NULL, 'Entecavir',       'إنتيكافير',         'Antiviral'),
  (NULL, 'Sofosbuvir',      'سوفوسبوفير',        'Antiviral'),
  -- Psychiatry / Neurology
  (NULL, 'Venlafaxine',     'فينلافاكسين',       'SNRI'),
  (NULL, 'Duloxetine',      'دولوكستين',         'SNRI'),
  (NULL, 'Paroxetine',      'باروكستين',         'SSRI'),
  (NULL, 'Mirtazapine',     'ميرتازابين',        'Antidepressant'),
  (NULL, 'Quetiapine',      'كويتيابين',         'Antipsychotic'),
  (NULL, 'Olanzapine',      'أولانزابين',        'Antipsychotic'),
  (NULL, 'Risperidone',     'ريسبيريدون',        'Antipsychotic'),
  (NULL, 'Haloperidol',     'هالوبيريدول',       'Antipsychotic'),
  (NULL, 'Levetiracetam',   'ليفيتيراسيتام',     'Anticonvulsant'),
  (NULL, 'Lamotrigine',     'لاموتريجين',        'Anticonvulsant'),
  (NULL, 'Topiramate',      'توبيراميت',         'Anticonvulsant'),
  (NULL, 'Donepezil',       'دونيبيزيل',         'Alzheimer drug'),
  (NULL, 'Memantine',       'ميمانتين',          'Alzheimer drug'),
  -- Respiratory
  (NULL, 'Tiotropium',      'تيوتروبيوم',        'LAMA'),
  (NULL, 'Formoterol',      'فورموتيرول',        'LABA'),
  (NULL, 'Salmeterol',      'سالميتيرول',        'LABA'),
  (NULL, 'Ipratropium',     'إبراتروبيوم',       'SAMA'),
  (NULL, 'Theophylline',    'ثيوفيلين',          'Bronchodilator'),
  -- Allergy / Immunology
  (NULL, 'Bilastine',       'بيلاستين',          'Antihistamine'),
  (NULL, 'Levocetirizine',  'ليفوسيتريزين',      'Antihistamine'),
  (NULL, 'Ketotifen',       'كيتوتيفين',         'Antihistamine'),
  (NULL, 'Hydroxyzine',     'هيدروكسيزين',       'Antihistamine'),
  -- Pain / MSK
  (NULL, 'Tramadol',        'ترامادول',          'Opioid analgesic'),
  (NULL, 'Codeine',         'كودايين',           'Opioid analgesic'),
  (NULL, 'Morphine',        'مورفين',            'Opioid analgesic'),
  (NULL, 'Fentanyl',        'فنتانيل',           'Opioid analgesic'),
  (NULL, 'Etoricoxib',      'إيتوريكوكسيب',      'NSAID'),
  (NULL, 'Celecoxib',       'سيليكوكسيب',        'NSAID'),
  (NULL, 'Aceclofenac',     'أسي كلوفيناك',      'NSAID'),
  (NULL, 'Thiocolchicoside', 'ثيوكولشيكوسيد',    'Muscle relaxant'),
  (NULL, 'Baclofen',        'باكلوفين',          'Muscle relaxant'),
  -- Urology / Hormonal
  (NULL, 'Tamsulosin',      'تامسولوسين',        'Alpha-blocker'),
  (NULL, 'Finasteride',     'فيناستيريد',        '5-alpha reductase inhibitor'),
  (NULL, 'Dutasteride',     'دوتاستيريد',        '5-alpha reductase inhibitor'),
  (NULL, 'Sildenafil',      'سيلدينافيل',        'PDE5 inhibitor'),
  (NULL, 'Tadalafil',       'تادالافيل',         'PDE5 inhibitor'),
  (NULL, 'Solifenacin',     'سوليفيناسين',       'Antimuscarinic'),
  (NULL, 'Tolterodine',     'تولتيرودين',        'Antimuscarinic'),
  -- Dermatology
  (NULL, 'Betamethasone',   'بيتاميثازون',       'Corticosteroid (topical)'),
  (NULL, 'Hydrocortisone Cream','كريم هيدروكورتيزون','Corticosteroid (topical)'),
  (NULL, 'Isotretinoin',    'إيزوتريتينوين',     'Retinoid'),
  (NULL, 'Adapalene',       'أدابالين',          'Retinoid (topical)'),
  (NULL, 'Benzoyl Peroxide','بيروكسيد البنزويل', 'Acne treatment')
ON CONFLICT (rxcui) DO NOTHING;

-- -------- More Egyptian brands --------
INSERT INTO products (drug_id, brand_en, brand_ar, market, manufacturer,
                     registration_no, form, strength, source)
SELECT d.id, v.brand_en, v.brand_ar, 'EG', v.manufacturer,
       v.reg_no, v.form, v.strength, 'EDA'
FROM (VALUES
    -- Cardiology brands
    ('Ramipril',        'Tritace',       'تريتاس',        'Sanofi',    'EDA-TRITACE-5',    'Tablet',  '5mg'),
    ('Perindopril',     'Coversyl',      'كوفرسيل',       'Servier',   'EDA-COVERSYL-5',   'Tablet',  '5mg'),
    ('Olmesartan',      'Olmetec',       'أولميتيك',      'Daiichi',   'EDA-OLMETEC-20',   'Tablet',  '20mg'),
    ('Telmisartan',     'Micardis',      'ميكارديس',      'Boehringer','EDA-MICARDIS-80',  'Tablet',  '80mg'),
    ('Nebivolol',       'Nebilet',       'نيبيليت',       'Berlin-Chemie','EDA-NEBILET-5', 'Tablet',  '5mg'),
    ('Ivabradine',      'Procoralan',    'بروكورالان',    'Servier',   'EDA-PROCORALAN-5', 'Tablet',  '5mg'),
    ('Amiodarone',      'Cordarone',     'كوردارون',      'Sanofi',    'EDA-CORDARONE-200','Tablet',  '200mg'),
    ('Ticagrelor',      'Brilinta',      'بريلينتا',      'AstraZeneca','EDA-BRILINTA-90', 'Tablet',  '90mg'),
    ('Ezetimibe',       'Ezetrol',       'إزيتيرول',      'MSD',       'EDA-EZETROL-10',   'Tablet',  '10mg'),
    ('Fenofibrate',     'Lipanthyl',     'ليبانثيل',      'Abbott',    'EDA-LIPANTHYL-200','Capsule', '200mg'),
    -- Diabetes
    ('Dapagliflozin',   'Forxiga',       'فورسيجا',       'AstraZeneca','EDA-FORXIGA-10',  'Tablet',  '10mg'),
    ('Linagliptin',     'Trajenta',      'تراجينتا',      'Boehringer','EDA-TRAJENTA-5',   'Tablet',  '5mg'),
    ('Saxagliptin',     'Onglyza',       'أونجليزا',      'AstraZeneca','EDA-ONGLYZA-5',   'Tablet',  '5mg'),
    ('Liraglutide',     'Victoza',       'فيكتوزا',       'Novo Nordisk','EDA-VICTOZA-1.8','Injection','1.8mg'),
    ('Insulin Aspart',  'NovoRapid',     'نوفورابيد',     'Novo Nordisk','EDA-NOVORAPID-100','Injection','100U/ml'),
    ('Insulin Detemir', 'Levemir',       'ليفيمير',       'Novo Nordisk','EDA-LEVEMIR-100','Injection','100U/ml'),
    ('Pioglitazone',    'Actos',         'أكتوس',         'Takeda',    'EDA-ACTOS-30',     'Tablet',  '30mg'),
    -- GI
    ('Rabeprazole',     'Pariet',        'بارييت',        'Janssen',   'EDA-PARIET-20',    'Tablet',  '20mg'),
    ('Sucralfate',      'Antepsin',      'أنتيبسين',      'Amriya',    'EDA-ANTEPSIN-1G',  'Suspension','1g'),
    ('Mesalazine',      'Pentasa',       'بنتازا',        'Ferring',   'EDA-PENTASA-500',  'Tablet',  '500mg'),
    -- Anti-infectives
    ('Cefuroxime',      'Zinnat',        'زينات',         'GSK',       'EDA-ZINNAT-500',   'Tablet',  '500mg'),
    ('Cefdinir',        'Omnicef',       'أومينيسف',      'Abbott',    'EDA-OMNICEF-300',  'Capsule', '300mg'),
    ('Ceftazidime',     'Fortum',        'فورتوم',        'GSK',       'EDA-FORTUM-1G',    'Injection','1g'),
    ('Meropenem',       'Meronem',       'ميرونيم',       'AstraZeneca','EDA-MERONEM-1G',  'Injection','1g'),
    ('Vancomycin',      'Vancocin',      'فانكوسين',      'Lilly',     'EDA-VANCOCIN-500', 'Injection','500mg'),
    ('Linezolid',       'Zyvox',         'زايفوكس',       'Pfizer',    'EDA-ZYVOX-600',    'Tablet',  '600mg'),
    ('Oseltamivir',     'Tamiflu',       'تاميفلو',       'Roche',     'EDA-TAMIFLU-75',   'Capsule', '75mg'),
    ('Valacyclovir',    'Valtrex',       'فالتريكس',      'GSK',       'EDA-VALTREX-500',  'Tablet',  '500mg'),
    ('Sofosbuvir',      'Sovaldi',       'سوفالدي',       'Gilead',    'EDA-SOVALDI-400',  'Tablet',  '400mg'),
    -- Psychiatry / Neurology
    ('Venlafaxine',     'Efexor',        'إيفيكسور',      'Pfizer',    'EDA-EFEXOR-75',    'Capsule', '75mg'),
    ('Duloxetine',      'Cymbalta',      'سيمبالتا',      'Lilly',     'EDA-CYMBALTA-30',  'Capsule', '30mg'),
    ('Paroxetine',      'Paxil',         'باكسيل',        'GSK',       'EDA-PAXIL-20',     'Tablet',  '20mg'),
    ('Mirtazapine',     'Remeron',       'ريمارون',       'MSD',       'EDA-REMERON-30',   'Tablet',  '30mg'),
    ('Quetiapine',      'Seroquel',      'سيروكويل',      'AstraZeneca','EDA-SEROQUEL-100','Tablet',  '100mg'),
    ('Olanzapine',      'Zyprexa',       'زيبريكسا',      'Lilly',     'EDA-ZYPREXA-10',   'Tablet',  '10mg'),
    ('Risperidone',     'Risperdal',     'ريسبيردال',     'Janssen',   'EDA-RISPERDAL-2',  'Tablet',  '2mg'),
    ('Haloperidol',     'Haldol',        'هالدول',        'Janssen',   'EDA-HALDOL-5',     'Tablet',  '5mg'),
    ('Levetiracetam',   'Keppra',        'كيبرا',         'UCB',       'EDA-KEPPRA-500',   'Tablet',  '500mg'),
    ('Lamotrigine',     'Lamictal',      'لاميكتال',      'GSK',       'EDA-LAMICTAL-100', 'Tablet',  '100mg'),
    ('Topiramate',      'Topamax',       'توباماكس',      'Janssen',   'EDA-TOPAMAX-50',   'Tablet',  '50mg'),
    ('Donepezil',       'Aricept',       'أريسيبت',       'Pfizer',    'EDA-ARICEPT-10',   'Tablet',  '10mg'),
    -- Respiratory
    ('Tiotropium',      'Spiriva',       'سبيريفا',       'Boehringer','EDA-SPIRIVA-INH',  'Inhaler', '18mcg'),
    ('Salmeterol',      'Serevent',      'سيريفنت',       'GSK',       'EDA-SEREVENT-INH', 'Inhaler', '25mcg'),
    ('Ipratropium',     'Atrovent',      'أتروفنت',       'Boehringer','EDA-ATROVENT-INH', 'Inhaler', '20mcg'),
    ('Theophylline',    'Euphyllin',     'يوفيلين',       'Sanofi',    'EDA-EUPHYLLIN-200','Tablet',  '200mg'),
    -- Allergy
    ('Bilastine',       'Bilaxten',      'بيلاكستن',      'Menarini',  'EDA-BILAXTEN-20',  'Tablet',  '20mg'),
    ('Levocetirizine',  'Xyzal',         'زيزال',         'UCB',       'EDA-XYZAL-5',      'Tablet',  '5mg'),
    ('Ketotifen',       'Zaditen',       'زاديتين',       'Novartis',  'EDA-ZADITEN-1',    'Tablet',  '1mg'),
    -- Pain
    ('Tramadol',        'Tramal',        'ترامال',        'Grunenthal','EDA-TRAMAL-50',    'Capsule', '50mg'),
    ('Etoricoxib',      'Arcoxia',       'أركويسا',       'MSD',       'EDA-ARCOXIA-90',   'Tablet',  '90mg'),
    ('Celecoxib',       'Celebrex',      'سيليبريكس',     'Pfizer',    'EDA-CELEBREX-200', 'Capsule', '200mg'),
    ('Aceclofenac',     'Airtal',        'إيرتال',        'Almirall',  'EDA-AIRTAL-100',   'Tablet',  '100mg'),
    ('Thiocolchicoside','Coltramyl',     'كولتراميل',     'Sanofi',    'EDA-COLTRAMYL-4',  'Capsule', '4mg'),
    ('Baclofen',        'Lioresal',      'ليوريسال',      'Novartis',  'EDA-LIORESAL-10',  'Tablet',  '10mg'),
    -- Urology
    ('Tamsulosin',      'Omnic',         'أومنيك',        'Astellas',  'EDA-OMNIC-0.4',    'Capsule', '0.4mg'),
    ('Finasteride',     'Proscar',       'بروسكار',       'MSD',       'EDA-PROSCAR-5',    'Tablet',  '5mg'),
    ('Dutasteride',     'Avodart',       'أفودارت',       'GSK',       'EDA-AVODART-0.5',  'Capsule', '0.5mg'),
    ('Sildenafil',      'Viagra',        'فياجرا',        'Pfizer',    'EDA-VIAGRA-50',    'Tablet',  '50mg'),
    ('Tadalafil',       'Cialis',        'سياليس',        'Lilly',     'EDA-CIALIS-20',    'Tablet',  '20mg'),
    ('Solifenacin',     'Vesicare',      'فيزيكير',       'Astellas',  'EDA-VESICARE-5',   'Tablet',  '5mg'),
    -- Dermatology
    ('Betamethasone',   'Betnovate',     'بيتنوفيت',      'GSK',       'EDA-BETNOVATE-CRM', 'Cream',  '0.1%'),
    ('Isotretinoin',    'Roaccutane',    'روأكيوتان',     'Roche',     'EDA-ROACCUTANE-20','Capsule', '20mg'),
    ('Adapalene',       'Differin',      'ديفرين',        'Galderma',  'EDA-DIFFERIN-GEL', 'Gel',     '0.1%'),
    ('Benzoyl Peroxide','Panoxyl',       'بانوكسيل',      'Stiefel',   'EDA-PANOXYL-GEL',  'Gel',     '5%')
) AS v(generic, brand_en, brand_ar, manufacturer, reg_no, form, strength)
JOIN drugs d ON d.generic_en = v.generic
ON CONFLICT (market, registration_no) DO NOTHING;