"""
defaults.py — Valores padrão para todas as secções do site e configurações de diretórios.
"""

from pathlib import Path

# Diretórios de Upload
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
PASTORAL_TEAM_UPLOADS_DIR = UPLOADS_DIR / "pastoral_team"
GALLERY_UPLOADS_DIR = UPLOADS_DIR / "gallery"
MINISTRIES_UPLOADS_DIR = UPLOADS_DIR / "ministries"

# Criar diretórios se não existirem
PASTORAL_TEAM_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
GALLERY_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
MINISTRIES_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# 1. WELCOME
DEFAULT_WELCOME_CONTENT = """
<p>Vem conhecer a ICMAV – Igreja Cristã Manancial de Águas Vivas.</p>
<p>Somos uma comunidade que celebra o amor de Deus, tendo como missão alcançar todas as pessoas para Jesus, conectando-as a um ambiente de família, ensinando-as a conhecer a fé em Cristo, capacitando-as a servir em excelência e amor ao próximo.</p>
<p>Esta também pode ser a tua casa.</p>
""".strip()

# 2. PURPOSES
DEFAULT_PURPOSES_CONTENT = [
    {
        "title": "Pertencer",
        "icon": "fas fa-users",
        "bgClass": "bg-primary",
        "desc": "Fomos chamados para pertencer à família de Deus, a igreja, sendo Seus filhos.",
        "biblicalPassage": "Mas a todos quantos O receberam deu-lhes o poder de serem feitos filhos de Deus: aos que creem no seu nome.",
        "biblicalReference": "João 1:12"
    },
    {
        "title": "Crescer",
        "icon": "fas fa-seedling",
        "bgClass": "bg-secondary",
        "desc": "Somos formados para sermos semelhantes a Jesus.",
        "biblicalPassage": "Sede meus imitadores, como também eu, de Cristo.",
        "biblicalReference": "1 Coríntios 11:1"
    },
    {
        "title": "Servir",
        "icon": "fas fa-hands-helping",
        "bgClass": "bg-green-500",
        "desc": "Somos motivados para servir as pessoas.",
        "biblicalPassage": "E ele mesmo deu uns para apóstolos, e outros para profetas, e outros para evangelistas, e outros para pastores e doutores.",
        "biblicalReference": "Efésios 4:11"
    },
    {
        "title": "Alcançar",
        "icon": "fas fa-globe",
        "bgClass": "bg-info",
        "desc": "Somos enviados para compartilhar esperança e vida em Jesus.",
        "biblicalPassage": "Ser-me-eis testemunhas tanto em Jerusalém como em toda a Judeia e Samaria e até aos confins da terra.",
        "biblicalReference": "Atos 1:8"
    },
    {
        "title": "Adorar",
        "icon": "fas fa-sun",
        "bgClass": "bg-yellow-300",
        "desc": "Fomos criados para adorar a Deus colocando-O em primeiro lugar nas nossas vidas.",
        "biblicalPassage": "Amarás, pois, o Senhor, teu Deus, de todo o teu coração, e de toda a tua alma, e de todo o teu poder.",
        "biblicalReference": "Deuteronómio 6:5"
    }
]

# 3. PASTORAL TEAM
DEFAULT_PASTORAL_TEAM_CONTENT = [
    {
        "id": 1,
        "name": "Pr Henrique\nPereira",
        "photo": "/src/assets/photos/people/henrique.jpg",
        "bio": """
        <p>Henrique Pereira é o pastor principal da nossa igreja e lidera com um coração cheio de alegria, humildade e dedicação ao serviço de Deus e das pessoas. Casado com Minita Pereira, são pais da Rute e do Marcos — que é casado com a Myriam — e avós orgulhosos da pequena Noa, a alegria da família.</p>
        <p>A sua jornada no ministério começou em 1989, ao lado da sua esposa, quando ambos serviram como pastores assistentes. Ao longo dos anos, têm sido uma presença constante na vida da comunidade, e em 2022 assumiram a liderança pastoral principal da igreja.</p>
        <p>O Pastor Henrique é conhecido pela sua proximidade com as pessoas, pela forma simples mas profunda como comunica a Palavra de Deus, e por ser alguém que ouve, cuida e caminha ao lado de quem o procura. A sua paixão é ver vidas transformadas pelo amor de Jesus — pessoas que descobrem que têm valor, propósito e um lugar na família de Deus. Para ele, a igreja deve ser um espaço onde todos são bem-vindos, independentemente do passado, onde há crescimento espiritual genuíno e onde a transformação acontece através do poder do Evangelho e da vivência em comunidade.</p>
        """.strip(),
        "spouseId": 2,
        "isLeadPair": True
    },
    {
        "id": 2,
        "name": "Pra Minita\nPereira",
        "photo": "/src/assets/photos/people/minita.jpg",
        "bio": """
        <p>Minita Pereira é esposa do Pastor Henrique e uma líder dedicada e inspiradora no seio da igreja. Com um coração cheio de empatia, sabedoria e sensibilidade espiritual, tem sido uma figura essencial na caminhada pastoral da comunidade desde 1989.</p>
        <p>Ao longo dos anos, Minita tem acompanhado muitas pessoas nas suas jornadas de fé, especialmente mulheres e famílias, com uma presença firme e encorajadora. É alguém que sabe escutar com atenção, orar com fé e apoiar com amor — sempre com um sorriso acolhedor e palavras de esperança.</p>
        <p>Enquanto mulher de fé, mãe e avó, Minita vive o ministério com naturalidade, integrando o cuidado da família com o cuidado da igreja. A sua vida é um reflexo do amor de Cristo em ação — discreta mas marcante, simples mas profunda. A sua visão, alinhada com a do Pastor Henrique, é ver uma igreja viva, acolhedora e centrada em Jesus — um lugar onde todos podem crescer, restaurar-se e descobrir o seu papel no plano de Deus.</p>
        """.strip(),
        "spouseId": 1,
        "isLeadPair": True
    },
    {
        "id": 3,
        "name": "Pr Rogério\nTrindade",
        "photo": "/src/assets/photos/people/rog.png",
        "bio": """
        <p>Rogério Trindade é casado com a Johana Antelo e têm dois filhos, o John e a Zoé. Nasceu na África do Sul, na cidade de Joganesburgo, fazendo parte de uma família de emigrantes portugueses e de cristãos comprometidos no serviço.</p>
        <p>Foi pastor titular durante 3 anos de uma igreja evangélica local em Espanha, na cidade de Sevilha. É pastor auxiliar na ICMAV desde 2016. É Líder-coordenador da ICMAV com Propósitos e dos Ministérios de Ligação. É também Diretor e formador da ICMAV COLLEGE. Foi fundador da Escola de Liderança com Propósitos (LCP) em 2015, nome anterior da escola. É autor de mais de 30 manuais de treinamento para líderes.</p>
        """.strip(),
        "spouseId": 4,
        "isLeadPair": False
    },
    {
        "id": 4,
        "name": "Pra Johana\nVillarroel",
        "photo": "/src/assets/photos/people/johana.png",
        "bio": """
        <p>Rosa Johana é casada com Rogério Trindade e têm dois filhos, o John e a Zoé. Nasceu na Bolívia, na cidade de Santa Cruz de la Sierra.</p>
        <p>Foi pastora titular acompanhada com o seu marido durante 3 anos de uma igreja evangélica local em Espanha, na cidade de Sevilha. É pastora auxiliar na ICMAV desde 2016. É responsável do propósito da adoração na equipa do ministério de crianças ALFA.</p>
        """.strip(),
        "spouseId": 3,
        "isLeadPair": False
    },
    {
        "id": 5,
        "name": "Pr Manza\nGarcia",
        "photo": "/src/assets/photos/people/manza.png",
        "bio": """
        <p>O Pr. Manza Garcia nasceu na República Democrática do Congo. Com 19 anos foi para Angola onde frequentou uma igreja baptista onde serviu a Deus como cantor durante 3 anos. A seguir foi para o sul de Angola durante 2 anos, voltando depois para Luanda onde começou o ministério como evangelista a pregar na igreja e em campanhas de massas com centenas de pessoas.</p>
        <p>Em 1989 veio para Portugal onde fundou uma igreja junto com uns amigos, onde ficou até 1995 quando o Pr. Leitão da igreja de Cascais o convidou para vir para a ICMAV, onde actualmente serve como pastor em Cascais e no Monte da Caparica.</p>
        <p>A ICMAV é uma igreja que está no seu coração, sendo uma comunidade que é relevante e que serve a Deus estendendo o Reino de Deus aqui na Terra. Acredita que a igreja não é para ser pequena, mas para crescer e continuar a ganhar espaço, querendo contribuir para esta expansão do Reino de Deus aqui na Terra na sua forma espiritual e física.</p>
        """.strip(),
        "spouseId": None,
        "isLeadPair": False
    },
    {
        "id": 6,
        "name": "Pr Paulo João\nCorreia",
        "photo": "/src/assets/photos/people/pj.png",
        "bio": """
        <p>Paulo João é pastor de louvor e adoração na ICMAV, onde também lidera o ministério de homens. Casado com Denise, é pai de dois filhos e avô da Salomé.</p>
        <p>A sua jornada no ministério começou aos 14 anos, após um encontro marcante com Jesus. Durante 18 anos serviu no Desafio Jovem, desenvolvendo trabalho evangelístico e social junto de comunidades vulneráveis e pessoas em situação de dependência.</p>
        <p>Desde 2006, dedica-se a tempo inteiro ao ministério pastoral, com ênfase no louvor, na formação de novas gerações e no discipulado de homens. A paternidade e a cultura do Reino no seio familiar são temas centrais da sua missão, procurando levantar líderes que vivam segundo o coração de Deus.</p>
        """.strip(),
        "spouseId": 7,
        "isLeadPair": False
    },
    {
        "id": 7,
        "name": "Pra Denise\nCorreia",
        "photo": "/src/assets/photos/people/denise.png",
        "bio": """
        <p>É esposa do Pastor Paulo João e tem sido, desde o início, uma companheira incansável no ministério. Embora não esteja à frente da adoração, a sua presença discreta e constante tem sido fundamental ao longo de toda a caminhada pastoral da família. Desde muito jovem, partilhou com o Paulo o chamado para servir, caminhando ao seu lado em todas as fases — desde os primeiros passos no ministério aos 14 anos, passando pelos anos intensos no Desafio Jovem, até ao serviço pastoral a tempo inteiro iniciado em 2006.</p>
        <p>Mãe de dois filhos e avó da pequena Salomé, Denise vive o seu ministério com o coração voltado para a família, o cuidado das pessoas e a edificação da Igreja. É uma mulher de oração, sensível à voz de Deus, e uma referência silenciosa de força, fé e dedicação. A sua missão não passa pelos holofotes, mas pela fidelidade no dia a dia, sempre disponível, sempre presente, sempre a semear amor.</p>
        """.strip(),
        "spouseId": 6,
        "isLeadPair": False
    },
    {
        "id": 8,
        "name": "Pr Danilo\nGujral",
        "photo": "/src/assets/photos/people/danilo.png",
        "bio": """
        <p>Nascido em Moçambique casado com Havani Gujral, pastor na ICMAV desde 2006 tendo já ocupado várias areas de ministério na igreja. Atualmente eles são responsáveis pelas várias equipas ligadas ao Propósito PERTENCER, que acompanham e apoiam quem nos visita até ao Batismo nas Águas ou Membresia na Igreja.</p>
        <p>Também supervisionam e treinam para o ministério das várias equipas do Celebrando Restauração da ICMAV. É produtor do programa radiofónico "Ponto de Encontro" dirigido aos solteiros, divorciados e viúvos uma parceria com a Rádio Transmundial de Portugal.</p>
        """.strip(),
        "spouseId": 9,
        "isLeadPair": False
    },
    {
        "id": 9,
        "name": "Pra Havani\nGujral",
        "photo": "/src/assets/photos/people/havani.png",
        "bio": """
        <p>Nascida no Brasil casada com Danilo Gujral, pastora na ICMAV desde 2006.</p>
        <p>Atualmente eles são responsáveis pelas várias equipas ligadas ao Propósito PERTENCER, que acompanham e apoiam quem nos visita até ao Batismo nas Águas ou Membresia na Igreja.</p>
        <p>Também supervisionam e treinam para o ministério das várias equipas do Celebrando Restauração da ICMAV.</p>
        """.strip(),
        "spouseId": 8,
        "isLeadPair": False
    },
    {
        "id": 10,
        "name": "Pr Carlos\nCardoso",
        "photo": "/src/assets/photos/people/carlitos.jpg",
        "bio": """
        <p>O Pastor Carlitos em Maio de 1998, num ciclo novo da sua vida, chegou para pastorear a Igreja Cristã Manancial de Águas Vivas (ICMAV). Liderou a Igreja por mais de vinte anos, onde viu Deus a abençoar o seu ministério e a igreja a multiplicar-se pela graça de Deus.</p>
        <p>Em Setembro de 2022, passou a liderança para o Pr. Henrique.</p>
        <p>Neste momento continua envolvido com esta comunidade como um dos pregadores habituais, como Pastor Conselheiro, juntamente com a sua esposa Isabel Cardoso, e também como professor da ICMAV College na promoção duma igreja com propósitos que seja relevante na comunidade, sempre com o entusiasmo e paixão que lhe são tão característicos.</p>
        """.strip(),
        "spouseId": 11,
        "isLeadPair": False
    },
    {
        "id": 11,
        "name": "Pra Isabel\nCardoso",
        "photo": "/src/assets/photos/people/nana.jpg",
        "bio": """
        <p>A pastora Isabel Cardoso (Nana) é uma pessoa com um coração sensível à presença de Deus, na sua chegada à ICMAV em Maio de 1998, estava a passar um tempo difícil na sua saúde, mas foi também o início de um processo onde alcançou a cura e restauração.</p>
        <p>Serviu com uma renovada paixão juntamente com o seu marido, por mais de vinte anos na Liderança principal da ICMAV.</p>
        <p>Hoje serve a Deus como Pastora conselheira, convicta que a ICMAV é um lugar onde vidas podem ser restauradas pela mensagem poderosa da Palavra de Deus, corações são sarados, e que Deus nunca desperdiça uma dor.</p>
        """.strip(),
        "spouseId": 10,
        "isLeadPair": False
    }
]

# 4. MESSAGE
DEFAULT_MESSAGE_CONTENT = """
<p>O nosso desejo é que cada pessoa que chegue até nós se sinta em casa, seja inspirada pela Palavra de Deus e encontre o apoio necessário para viver uma vida plena e com muito significado.</p>
<p>És muito bem-vindo à nossa comunidade</p>
<p>Queremos muito conhecer-te e partilhar contigo a alegria de caminhar na fé juntos!</p>
""".strip()

# 5. MINISTRIES PRESENTATION
DEFAULT_MINISTRIES_PRESENTATION_CONTENT = [
    {
        "name": "Mulheres",
        "slug": "mulheres",
        "icon": "fas fa-female",
        "bgClass": "bg-info",
        "desc": "Um grupo de mulheres que merece um espaço onde é ouvida, valorizada e encorajada.",
        "longDescription": [
            "O ministério de Mulheres é um espaço pensado para acolher, encorajar e fortalecer mulheres em todas as fases da vida. Através de estudos bíblicos, oração e partilha, criamos um ambiente seguro onde cada mulher pode crescer na fé, aprofundar a sua relação com Deus e construir amizades significativas.",
            "Os nossos encontros incluem workshops, palestras, tempos de louvor e eventos especiais que tocam em temas relevantes do dia a dia — sempre com o objetivo de trazer inspiração, cura, renovação e um sentido mais profundo de propósito.",
            "Acreditamos que cada mulher tem um valor único e um chamado divino, e queremos caminhar juntas nesta jornada, apoiando-nos umas às outras com graça, verdade e alegria."
        ],
        "leader": "Cristina Silva",
        "leaderPhoto": "/src/assets/photos/people/cristina.png",
        "contact": "+351 912 000 555",
        "media": {
            "type": "video",
            "src": "/src/assets/videos/hero.mp4",
            "placeholder": "/src/assets/fallbacks/hero.jpg"
        },
        "socialMedia": [
            {"icon": "fab fa-instagram", "link": "https://instagram.com/icmav_mulheres"}
        ]
    },
    {
        "name": "Homens",
        "slug": "homens",
        "icon": "fas fa-hands-helping",
        "bgClass": "bg-warning",
        "desc": "Grupo de camaradagem, troca e crescimento para todas as fases da vida .",
        "longDescription": [
            "O ministério de Homens é um espaço onde homens de todas as idades se juntam para crescer na fé e nas relações uns com os outros. Através de estudos bíblicos, conversas honestas e atividades ao ar livre, queremos promover uma caminhada cristã autêntica, com foco no discipulado e no fortalecimento da identidade em Cristo.",
            "Mais do que encontros pontuais, este ministério é uma rede de apoio e amizade. Organizamos retiros, caminhadas, pequenos-almoços e grupos de partilha onde os homens podem abrir o coração, partilhar lutas e celebrar vitórias num ambiente de confiança, respeito e encorajamento mútuo.",
            "Acreditamos que cada homem tem um papel essencial na família, na igreja e na sociedade — e queremos ser parte ativa no processo de crescimento espiritual, emocional e relacional de cada um."
        ],
        "leader": "Paulo João Correia",
        "leaderPhoto": "/src/assets/photos/people/pj.png",
        "contact": "+351 912 000 444",
        "media": {
            "type": "video",
            "src": "/src/assets/videos/hero.mp4",
            "placeholder": "/src/assets/fallbacks/hero.jpg"
        },
        "socialMedia": [
            {"icon": "fab fa-instagram", "link": "https://instagram.com/icmav_homens"}
        ]
    },
    {
        "name": "Casais",
        "slug": "casais",
        "icon": "fas fa-globe",
        "bgClass": "bg-error",
        "desc": "Porque cuidar do relacionamento a dois também é uma forma de amar.",
        "longDescription": [
            "O ministério de Casais existe para apoiar e fortalecer os relacionamentos, ajudando cada casal a crescer em amor, unidade e propósito. Promovemos encontros com temas relevantes, palestras, momentos de oração e dinâmicas práticas baseadas nos princípios da Palavra de Deus.",
            "Acreditamos que um casamento saudável não acontece por acaso — é construído com intencionalidade, comunicação e graça. Por isso, oferecemos acompanhamento pastoral, aconselhamento e espaços de partilha onde os casais podem aprender, rir, chorar e crescer juntos.",
            "Também organizamos conferências e retiros especiais que proporcionam tempo de qualidade a dois, ferramentas para lidar com desafios e oportunidades para renovar os votos e a visão do casamento. Queremos ver famílias fortes, resilientes e cheias de fé a impactar o mundo à sua volta."
        ],
        "leader": "Pedro Mateus",
        "leaderPhoto": "/src/assets/photos/people/pedro-mateus.png",
        "contact": "+351 912 000 666",
        "media": {
            "type": "video",
            "src": "/src/assets/videos/hero.mp4",
            "placeholder": "/src/assets/fallbacks/hero.jpg"
        },
        "socialMedia": [
            {"icon": "fab fa-instagram", "link": "https://instagram.com/icmav_casais"}
        ]
    },
    {
        "name": "Jovens",
        "slug": "jovens",
        "icon": "fas fa-heart",
        "bgClass": "bg-secondary",
        "desc": "Bora lá viver que vai além do comum, com propósito e significado.",
        "longDescription": [
            "Os encontros de Jovens juntam pessoas dos 18 aos 30 anos num ambiente descontraído, cheio de propósito. São momentos marcados por adoração, estudo da Palavra e partilha de vida — um espaço seguro para fazer perguntas, crescer na fé e construir amizades verdadeiras.",
            "Queremos inspirar esta geração a viver uma fé viva e prática, que se reflete nas escolhas diárias, no trabalho, na universidade, em casa e nas relações. Acreditamos que seguir Jesus é uma aventura transformadora que começa no coração e impacta tudo à volta.",
            "Para além dos encontros quinzenais, dinamizamos seminários, missões urbanas e outros eventos que fortalecem a ligação com Deus e com a cidade. Cada jovem é desafiado a descobrir o seu chamado e a ser luz onde quer que esteja — com coragem, criatividade e compaixão."
        ],
        "leader": "Marcos Pereira",
        "leaderPhoto": "/src/assets/photos/people/marcos.png",
        "contact": "+351 912 000 333",
        "media": {
            "type": "video",
            "src": "/src/assets/videos/hero.mp4",
            "placeholder": "/src/assets/fallbacks/hero.jpg"
        },
        "socialMedia": [
            {"icon": "fab fa-instagram", "link": "https://instagram.com/icyouth"}
        ]
    },
    {
        "name": "Teens",
        "slug": "teens",
        "icon": "fas fa-music",
        "bgClass": "bg-primary",
        "desc": "Aqui é onde começa a tua jornada: com gente real e fé prática.",
        "longDescription": [
            "O grupo Teens é um espaço vibrante, pensado especialmente para adolescentes que estão a descobrir quem são e em que acreditam. Aqui, combinamos momentos de louvor, conversas reais e oficinas criativas que incentivam a expressão pessoal, sempre com base em princípios cristãos.",
            "Queremos criar um ambiente onde cada jovem se sinta valorizado, ouvido e desafiado a crescer — não só na fé, mas também nas relações, no caráter e nas escolhas do dia a dia.",
            "Ao longo do ano, organizamos retiros, encontros temáticos e iniciativas solidárias que desenvolvem a liderança, o espírito de equipa e o sentido de missão. É uma oportunidade única para fazer amigos, servir, descobrir o propósito pessoal e aprender a viver com responsabilidade e intencionalidade."
        ],
        "leader": "João Maria Guedelha",
        "leaderPhoto": "/src/assets/photos/people/joao-maria.png",
        "contact": "+351 912 000 222",
        "media": {
            "type": "video",
            "src": "/src/assets/videos/teens.mp4",
            "placeholder": "/src/assets/fallbacks/hero.jpg"
        },
        "socialMedia": [
            {"icon": "fab fa-instagram", "link": "https://instagram.com/icteens"}
        ]
    },
    {
        "name": "Crianças",
        "slug": "criancas",
        "icon": "fas fa-hands-holding-child",
        "bgClass": "bg-accent",
        "desc": "Aqui a imaginação voa e o coração aprende o que realmente importa.",
        "longDescription": [
            "O ministério das crianças é um espaço cheio de alegria, criatividade e crescimento. Em cada encontro, as crianças são convidadas a mergulhar nas histórias da Bíblia de forma divertida e acessível — através de teatro, música, jogos e atividades que despertam a imaginação e mostram, de forma simples e verdadeira, o amor de Deus.",
            "Durante a série ALFA Kids, promovemos momentos especiais que envolvem tanto as crianças como os pais. São experiências pensadas para fortalecer os laços familiares e, ao mesmo tempo, lançar as bases da fé no coração dos mais novos. Acreditamos que a caminhada com Deus começa em casa e queremos caminhar ao lado das famílias nesse processo.",
            "Para além dos encontros semanais, organizamos também eventos temáticos em datas especiais como a Páscoa, o Natal ou o Dia da Criança. Tudo acontece num ambiente seguro, acolhedor e com uma equipa dedicada que cuida, ensina e brinca com os mais pequenos com muito carinho."
        ],
        "leader": "Patricia Pinto",
        "leaderPhoto": "/src/assets/photos/people/patricia.png",
        "contact": "+351 912 000 111",
        "media": {
            "type": "video",
            "src": "/src/assets/videos/hero.mp4",
            "placeholder": "/src/assets/fallbacks/hero.jpg"
        },
        "socialMedia": [
            {"icon": "fab fa-instagram", "link": "https://instagram.com/alfa.icmav"}
        ]
    }
]

# 6. SERVICES BANNER
DEFAULT_SERVICES_BANNER_CONTENT = """
<p>Vista-nos aos domingos numa das nossas localizações.</p>
""".strip()

# 7. LOCAL GATHERINGS
DEFAULT_LOCAL_GATHERINGS_CONTENT = {
    "localGatheringsQuote": "Uma comunidade saudável é ser grande e pequena ao mesmo tempo.",
    "localGatheringsQuoteReference": "Rick Warren",
    "localGatheringsBody": """
        <p>Acreditamos que relações de confiança e proximidade são essenciais para quem está a construir uma vida saudável.</p>
        <p>Foi essa a conclusão mais forte de um inquérito que fizemos em 2011, dentro e fora da ICMAV. Deus tem uma família, e queremos que tu também faças parte dela.</p>
        <p>Os Pequenos Grupos são uma forma de viver a fé de maneira próxima, em encontros semanais, quinzenais ou mensais, com grupos pensados para diferentes interesses e faixas etárias.</p>
        <p>Preenche o formulário abaixo e junta-te a um Pequeno Grupo feito para ti.</p>
    """.strip()
}

# 8. LOCAL GATHERING OPTIONS
DEFAULT_LOCAL_GATHERING_OPTIONS = [
    {
        "slug": "pg-carcavelos-casais",
        "leaderName": "João e Marta Silva",
        "emailContact": "xpto@testtest.com",
        "characteristicTag": "Casais",
        "location": "Carcavelos"
    },
    {
        "slug": "pg-amadora-jovens-adultos",
        "leaderName": "Daniel Ferreira",
        "emailContact": "xpto@testtest.com",
        "characteristicTag": "Jovens Adultos",
        "location": "Amadora"
    },
    {
        "slug": "pg-almada-familias",
        "leaderName": "Ana Ribeiro",
        "emailContact": "xpto@testtest.com",
        "characteristicTag": "Famílias",
        "location": "Almada"
    },
    {
        "slug": "pg-oeiras-seniores",
        "leaderName": "Carlos Mendes",
        "emailContact": "xpto@testtest.com",
        "characteristicTag": "Seniores",
        "location": "Oeiras"
    }
]

# 9. GALLERY
DEFAULT_GALLERY_CONTENT = [
    "/src/assets/photos/gallery/gallery2.png",
    "/src/assets/photos/gallery/gallery3.png",
    "/src/assets/photos/gallery/gallery4.png",
    "/src/assets/photos/gallery/gallery5.png",
    "/src/assets/photos/gallery/gallery3.png",
]

# 10. SOCIAL MEDIA
DEFAULT_SOCIAL_MEDIA_CONTENT = [
    {
        "icon": "fa-brands fa-facebook-f",
        "link": "https://facebook.com/icmav",
        "hoverColor": "#60A5FA"
    },
    {
        "icon": "fa-brands fa-instagram",
        "link": "https://instagram.com/icmav",
        "hoverColor": "#F472B6"
    },
    {
        "icon": "fa-brands fa-youtube",
        "link": "https://www.youtube.com/@igrejaICMAV",
        "hoverColor": "#F87171"
    },
    {
        "icon": "fa-brands fa-whatsapp",
        "link": "https://chat.whatsapp.com/EdGaqNUARdYB7HokXeleHR",
        "hoverColor": "#4ADE80"
    }
]

# 11. DONATIONS (com dados bancários e categorias de contribuição)
DEFAULT_DONATIONS_CONTENT = {
    "donationsBody": """
        <p>A tua contribuição faz a diferença.</p>
        <p>Cada contribuição é recebida com gratidão, responsabilidade e transparência.</p>
        <p>Ajuda-nos a continuar esta missão com fé, serviço e generosidade.</p>
    """.strip(),
    "donationsQuote": "Cada um contribua segundo propôs no seu coração; não com tristeza, ou por necessidade; porque Deus ama ao que dá com alegria.",
    "donationsQuoteAuthor": "2 Coríntios 9:7",
    "beneficiary": "Igreja Cristã Manancial de Águas Vivas",
    "iban": "PT50 0007 0246 0014 0750 0033 4",
    "bank": "NOVO BANCO, SA",
    "bic": "BESCPTPLXXX",
    "treasuryEmail": "tesouraria.icmav@gmail.com",
    "categories": [
        {"id": "Ofertas", "name": "Ofertas"},
        {"id": "Dízimos", "name": "Dízimos"},
        {"id": "Missões", "name": "Missões"},
    ]
}

# 12. LOCATIONS
MAP_CENTER_LAT_OFFSET = -0.000075
MAP_CENTER_LNG_OFFSET = -0.005000

DEFAULT_LOCATIONS_RAW = [
    {
        "slug": "sede",
        "name": "São Domingos de Rana",
        "type": "Sede",
        "email": "ccicmav@gmail.com",
        "phone": "+351 934 693 310",
        "address": "Estrada de Polima N.º 609, 2785-303 Polima",
        "mapsLink": "https://maps.app.goo.gl/VJ81xhdhP7h4WpeW7",
        "customWebsite": None,
        "sundayService": "10h30",
        "markerPosition": "38.724251,-9.327461",
        "mapZoom": 17
    },
    {
        "slug": "caparica",
        "name": "Caparica",
        "type": "Extensão",
        "email": "icmavmontedecaparica@gmail.com",
        "phone": "+351 934 693 310",
        "address": "Rua de Bela Vista N.º 110 R/C-A, 2825-165 Caparica",
        "mapsLink": "https://maps.app.goo.gl/N8iRjQeHSWMBXfZL6",
        "customWebsite": None,
        "sundayService": "16h30",
        "markerPosition": "38.667462,-9.191447",
        "mapZoom": 17
    },
    {
        "slug": "londres",
        "name": "Londres",
        "type": "Extensão",
        "email": "church@icmavlondon.com",
        "phone": "+44 4794 0509951",
        "address": "125 Gibraltar Crescent, Epsom Londres",
        "mapsLink": "https://maps.app.goo.gl/SkEZUHQSK2igi6QEA",
        "customWebsite": "icmavlondon.com",
        "sundayService": "17h00",
        "markerPosition": "51.346883,-0.262277",
        "mapZoom": 17
    }
]
# 13. SIBS GATEWAY CONFIG (sem defaults)
DEFAULT_SIBS_CONFIG = {
    "sibs_api_base": "",
    "sibs_bearer_token": "",
    "sibs_client_id": "",
    "sibs_client_secret": "",
    "sibs_terminal_id": "",
}

def calculate_map_center(marker_pos: str) -> str:
    parts = marker_pos.split(",")
    lat = float(parts[0].strip()) + MAP_CENTER_LAT_OFFSET
    lng = float(parts[1].strip()) + MAP_CENTER_LNG_OFFSET
    return f"{lat:.6f},{lng:.6f}"


DEFAULT_LOCATIONS_CONTENT = [
    {**loc, "mapCenter": calculate_map_center(loc["markerPosition"])}
    for loc in DEFAULT_LOCATIONS_RAW
]
