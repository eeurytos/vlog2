from main import app, db, Category, Post
from datetime import datetime

def init_test_data():
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        
        # Kategorileri ekle
        categories = [
            "Teknoloji",
            "Yazılım Geliştirme",
            "Web Tasarım",
            "Mobil Uygulama",
            "Veri Bilimi",
            "Yapay Zeka",
            "Siber Güvenlik",
            "DevOps"
        ]
        
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                category = Category(name=cat_name)
                db.session.add(category)
        
        db.session.commit()
        print("Kategoriler eklendi.")
        
        # Test yazılarını ekle
        test_posts = [
            {
                "title": "Python ile Web Geliştirme: Flask Framework",
                "preview": "Flask, Python'da web uygulamaları geliştirmek için kullanılan hafif ve esnek bir framework'tür.",
                "content": """
                <h2>Flask Framework Nedir?</h2>
                <p>Flask, Python programlama dili için geliştirilmiş bir web framework'üdür. Mikro framework olarak adlandırılır çünkü minimum dış bağımlılık gerektirir.</p>
                
                <h3>Flask'in Avantajları</h3>
                <ul>
                    <li>Basit ve anlaşılır yapı</li>
                    <li>Hızlı geliştirme imkanı</li>
                    <li>Esnek mimari</li>
                    <li>Geniş eklenti desteği</li>
                </ul>

                <h3>Örnek Kullanım Alanları</h3>
                <p>Flask ile API servisleri, web siteleri, admin panelleri ve daha birçok web uygulaması geliştirebilirsiniz.</p>
                """,
                "category_name": "Web Tasarım",
                "reading_time": 6
            },
            {
                "title": "Yapay Zeka ve Makine Öğrenimi Temelleri",
                "preview": "Yapay zeka ve makine öğrenimi alanındaki temel kavramlar ve güncel gelişmeler.",
                "content": """
                <h2>Yapay Zeka Nedir?</h2>
                <p>Yapay zeka, insan zekasını taklit eden ve topladığı bilgilere göre kendini geliştirebilen sistemlerdir.</p>

                <h3>Makine Öğrenimi Türleri</h3>
                <ul>
                    <li>Denetimli Öğrenme</li>
                    <li>Denetimsiz Öğrenme</li>
                    <li>Pekiştirmeli Öğrenme</li>
                </ul>

                <h3>Güncel Uygulamalar</h3>
                <p>Görüntü işleme, doğal dil işleme ve robotik gibi alanlarda yapay zeka yaygın olarak kullanılmaktadır.</p>
                """,
                "category_name": "Yapay Zeka",
                "reading_time": 8
            },
            {
                "title": "Modern Web Güvenliği ve OWASP Top 10",
                "preview": "Web uygulamalarında güvenlik açıklarına karşı alınması gereken önlemler ve OWASP Top 10 listesi.",
                "content": """
                <h2>Web Güvenliği Neden Önemli?</h2>
                <p>Web uygulamalarının güvenliği, kullanıcı verilerinin korunması ve sistemin sürdürülebilirliği açısından kritik öneme sahiptir.</p>

                <h3>OWASP Top 10 Güvenlik Riskleri</h3>
                <ul>
                    <li>Enjeksiyon Saldırıları</li>
                    <li>Kimlik Doğrulama Zafiyetleri</li>
                    <li>Hassas Veri İfşası</li>
                    <li>XML Dış Varlık Referansları</li>
                </ul>

                <h3>Güvenlik Önlemleri</h3>
                <p>Güvenli kod yazma pratikleri, düzenli güvenlik testleri ve güncel güvenlik yamalarının takibi önemlidir.</p>
                """,
                "category_name": "Siber Güvenlik",
                "reading_time": 7
            },
            {
                "title": "Veri Bilimi ve Python Kütüphaneleri",
                "preview": "Veri bilimi projelerinde sıklıkla kullanılan Python kütüphaneleri ve kullanım alanları.",
                "content": """
                <h2>Veri Biliminde Python</h2>
                <p>Python, zengin kütüphane ekosistemi sayesinde veri bilimi alanında en çok tercih edilen programlama dillerinden biridir.</p>

                <h3>Temel Kütüphaneler</h3>
                <ul>
                    <li>NumPy: Sayısal işlemler ve diziler</li>
                    <li>Pandas: Veri analizi ve manipülasyonu</li>
                    <li>Matplotlib: Veri görselleştirme</li>
                    <li>Scikit-learn: Makine öğrenimi</li>
                </ul>

                <h3>Veri Analizi Süreci</h3>
                <p>Veri toplama, temizleme, analiz ve görselleştirme aşamalarında Python kütüphaneleri etkin şekilde kullanılır.</p>
                """,
                "category_name": "Veri Bilimi",
                "reading_time": 5
            },
            {
                "title": "Docker ve Konteynerleştirme Teknolojileri",
                "preview": "Docker kullanarak uygulamaları konteynerleştirme ve mikroservis mimarisi.",
                "content": """
                <h2>Docker Nedir?</h2>
                <p>Docker, uygulamaları konteynerler içinde paketleyerek taşınabilir ve ölçeklenebilir hale getiren bir platformdur.</p>

                <h3>Docker'ın Avantajları</h3>
                <ul>
                    <li>Kolay dağıtım ve ölçeklendirme</li>
                    <li>İzole çalışma ortamı</li>
                    <li>Kaynak verimliliği</li>
                    <li>Hızlı geliştirme süreci</li>
                </ul>

                <h3>Temel Docker Komutları</h3>
                <p>Docker run, build, push gibi temel komutlarla konteyner yaşam döngüsü yönetilir.</p>
                """,
                "category_name": "DevOps",
                "reading_time": 6
            }
        ]

        # Test yazılarını veritabanına ekle
        for post_data in test_posts:
            category = Category.query.filter_by(name=post_data['category_name']).first()
            if category and not Post.query.filter_by(title=post_data['title']).first():
                post = Post(
                    title=post_data['title'],
                    preview=post_data['preview'],
                    content=post_data['content'],
                    category_id=category.id,
                    reading_time=post_data['reading_time']
                )
                db.session.add(post)
        
        db.session.commit()
        print("Test yazıları eklendi.")

if __name__ == "__main__":
    init_test_data() 