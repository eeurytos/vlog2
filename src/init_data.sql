
-- Blog yazılarını ekle
INSERT INTO post (title, slug, preview, content, category_id, reading_time, created_at) VALUES 
(
    'Python ile Web Geliştirme: Flask Framework',
    'python-ile-web-gelistirme-flask-framework',
    'Flask, Python''da web uygulamaları geliştirmek için kullanılan hafif ve esnek bir framework''tür.',
    '<h2>Flask Framework Nedir?</h2>
    <p>Flask, Python programlama dili için geliştirilmiş bir web framework''üdür. Mikro framework olarak adlandırılır çünkü minimum dış bağımlılık gerektirir.</p>
    
    <h3>Flask''in Avantajları</h3>
    <ul>
        <li>Basit ve anlaşılır yapı</li>
        <li>Hızlı geliştirme imkanı</li>
        <li>Esnek mimari</li>
        <li>Geniş eklenti desteği</li>
    </ul>

    <h3>Örnek Kullanım Alanları</h3>
    <p>Flask ile API servisleri, web siteleri, admin panelleri ve daha birçok web uygulaması geliştirebilirsiniz.</p>',
    (SELECT id FROM category WHERE slug = 'web-tasarim'),
    6,
    CURRENT_TIMESTAMP
),
(
    'Yapay Zeka ve Makine Öğrenimi Temelleri',
    'yapay-zeka-ve-makine-ogrenimi-temelleri',
    'Yapay zeka ve makine öğrenimi alanındaki temel kavramlar ve güncel gelişmeler.',
    '<h2>Yapay Zeka Nedir?</h2>
    <p>Yapay zeka, insan zekasını taklit eden ve topladığı bilgilere göre kendini geliştirebilen sistemlerdir.</p>

    <h3>Makine Öğrenimi Türleri</h3>
    <ul>
        <li>Denetimli Öğrenme</li>
        <li>Denetimsiz Öğrenme</li>
        <li>Pekiştirmeli Öğrenme</li>
    </ul>

    <h3>Güncel Uygulamalar</h3>
    <p>Görüntü işleme, doğal dil işleme ve robotik gibi alanlarda yapay zeka yaygın olarak kullanılmaktadır.</p>',
    (SELECT id FROM category WHERE slug = 'yapay-zeka'),
    8,
    CURRENT_TIMESTAMP
),
(
    'Modern Web Güvenliği ve OWASP Top 10',
    'modern-web-guvenligi-ve-owasp-top-10',
    'Web uygulamalarında güvenlik açıklarına karşı alınması gereken önlemler ve OWASP Top 10 listesi.',
    '<h2>Web Güvenliği Neden Önemli?</h2>
    <p>Web uygulamalarının güvenliği, kullanıcı verilerinin korunması ve sistemin sürdürülebilirliği açısından kritik öneme sahiptir.</p>

    <h3>OWASP Top 10 Güvenlik Riskleri</h3>
    <ul>
        <li>Enjeksiyon Saldırıları</li>
        <li>Kimlik Doğrulama Zafiyetleri</li>
        <li>Hassas Veri İfşası</li>
        <li>XML Dış Varlık Referansları</li>
    </ul>

    <h3>Güvenlik Önlemleri</h3>
    <p>Güvenli kod yazma pratikleri, düzenli güvenlik testleri ve güncel güvenlik yamalarının takibi önemlidir.</p>',
    (SELECT id FROM category WHERE slug = 'siber-guvenlik'),
    7,
    CURRENT_TIMESTAMP
),
(
    'Veri Bilimi ve Python Kütüphaneleri',
    'veri-bilimi-ve-python-kutuphaneleri',
    'Veri bilimi projelerinde sıklıkla kullanılan Python kütüphaneleri ve kullanım alanları.',
    '<h2>Veri Biliminde Python</h2>
    <p>Python, zengin kütüphane ekosistemi sayesinde veri bilimi alanında en çok tercih edilen programlama dillerinden biridir.</p>

    <h3>Temel Kütüphaneler</h3>
    <ul>
        <li>NumPy: Sayısal işlemler ve diziler</li>
        <li>Pandas: Veri analizi ve manipülasyonu</li>
        <li>Matplotlib: Veri görselleştirme</li>
        <li>Scikit-learn: Makine öğrenimi</li>
    </ul>

    <h3>Veri Analizi Süreci</h3>
    <p>Veri toplama, temizleme, analiz ve görselleştirme aşamalarında Python kütüphaneleri etkin şekilde kullanılır.</p>',
    (SELECT id FROM category WHERE slug = 'veri-bilimi'),
    5,
    CURRENT_TIMESTAMP
),
(
    'Docker ve Konteynerleştirme Teknolojileri',
    'docker-ve-konteyner-teknolojileri',
    'Docker kullanarak uygulamaları konteynerleştirme ve mikroservis mimarisi.',
    '<h2>Docker Nedir?</h2>
    <p>Docker, uygulamaları konteynerler içinde paketleyerek taşınabilir ve ölçeklenebilir hale getiren bir platformdur.</p>

    <h3>Docker''ın Avantajları</h3>
    <ul>
        <li>Kolay dağıtım ve ölçeklendirme</li>
        <li>İzole çalışma ortamı</li>
        <li>Kaynak verimliliği</li>
        <li>Hızlı geliştirme süreci</li>
    </ul>

    <h3>Temel Docker Komutları</h3>
    <p>Docker run, build, push gibi temel komutlarla konteyner yaşam döngüsü yönetilir.</p>',
    (SELECT id FROM category WHERE slug = 'devops'),
    6,
    CURRENT_TIMESTAMP
); 