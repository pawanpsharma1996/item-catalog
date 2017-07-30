# all file imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Items

engine = create_engine('sqlite:///itemcatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# data for cricket
category1 = Categories(name="Cricket")
session.add(category1)
session.commit()

item1 = Items(
    name="Willow Bat",
    category="Cricket",
    description="Once you start hardball it is recommended you use an English willow bat, due to a significant performance advantage. The ball will travel much easier and quicker"
)
session.add(item1)
session.commit()

item2 = Items(
    name="Leather Ball",
    description="The Club is a high quality four-piece cricket ball made from high quality alum tanned leather; The Club is ideally suited for club and school matches",
    categories=category1)
session.add(item2)
session.commit()

item3 = Items(
    name="Knee Pad",
    description="Pads (also called leg guards) are protective equipment used by batters in the sports of cricket ... Batting pads protect the shins, knees and the lower thigh.",
    categories=category1)
session.add(item3)
session.commit()

# data for football
category2 = Categories(name="FootBall")
session.add(category2)
session.commit()

item1 = Items(
    name="Ball",
    categories=category2,
    description="Strike Football, Size 5 (White/Purple) Rs. 500.00. ... Nike Strike-Hi-Vis Football, Size 5 (Yellow/Black/Purple) ... The Nike Strike Premier League Football is competition-ready with high-contrast graphics for better ball tracking and a reinforced rubber bladder for a"
)
session.add(item1)
session.commit()

item2 = Items(
    name="Jersy",
    description="Design custom football jerseys for your team or event online. Free Shipping, Live Help and thousands of design ideas. Add Names and Numbers.",
    categories=category2)
session.add(item2)
session.commit()

# data for basketball
category3 = Categories(name="BasketBall")
session.add(category3)
session.commit()

item1 = Items(
    name="Ball",
    categories=category3,
    description="Well, explore a wide range from Nike, Spalding, Cosco, Nivia and more. Available in different colours, Spalding basketballs are the rage among all basketball lovers. ... From basketball nets to basketball rings, you'll find everything on Snapdeal."
)
session.add(item1)
session.commit()

item2 = Items(
    name="Net",
    description="If you are looking at buying a basketball ring, portable basketball stand, basketball set or basketball net, our online shopping site has it all.",
    categories=category3)
session.add(item2)
session.commit()

# data for hockey
category4 = Categories(name="Hockey")
session.add(category4)
session.commit()

item1 = Items(
    name="Hockey Stick",
    categories=category4,
    description="Buy from HockeyMonkey's selection of intermediate hockey sticks. Select intermediate sticks from top brands like Bauer, CCM, Warrior, Sherwood and many "
)
session.add(item1)
session.commit()

item2 = Items(
    name="Ball",
    description="Field Hockey from a great selection at Sports, Fitness & Outdoors Store.",
    categories=category4)
session.add(item2)
session.commit()

# data for tennis
category5 = Categories(name="Tennis")
session.add(category5)
session.commit()

item1 = Items(
    name="Tennis Racquet",
    categories=category5,
    description="We carry a giant selection and have a racquet for every player. If you are looking for control tennis racquets, power racquets, or a racquet in between, we've got the racquet for you. We offer tennis racquets in all price ranges, and we carry the most popular tennis brands, including Wilson, Head, and Babolat. "
)
session.add(item1)
session.commit()

item2 = Items(
    name="Net",
    description="Edwards 40-LS 3.5MM Double Canvas Tennis Nets. Price: $ ... Edwards 3.0MM DBL Center Outback Tennis Nets ... Quik-Stiks Tennis Singles Net Sticks Black.",
    categories=category5)
session.add(item2)
session.commit()

# data for snowboarding
category6 = Categories(name="SnowBoarding")
session.add(category6)
session.commit()

item1 = Items(
    name="SnowBoard",
    categories=category6,
    description="Snowboard Car Racks Car Racks. Body Armor. Parts & Accessories. Find more discount snowboard gear in outlet. Outlet Snowboard Shop. Burton. Lib Tech "
)
session.add(item1)
session.commit()

item2 = Items(
    name="Goggles",
    description="Snowboard Goggles ... Electric EG2.5 Goggles $159.95 - $179.95 $91.79 - $106.24 LimitedTime ... Dragon D1 OTG Goggles $59.95 $47.96 LimitedTime.",
    categories=category6)
session.add(item2)
session.commit()

# data for Rock Climbing
category7 = Categories(name="Rock Climbing")
session.add(category7)
session.commit()

item1 = Items(
    name="Carabiners",
    categories=category7,
    description="Carabiners are metal loops with spring-loaded"
	" gates (openings), used as connectors. Once made"
	" primarily from steel, almost all carabiners for "
	"recreational climbing are now made from a light weight"
	" aluminum alloy. Steel carabiners are much heavier, but"
	" harder wearing, and therefore are often used by"
	" instructors when working with groups. "
)
session.add(item1)
session.commit()

item2 = Items(
    name="Harnesses",
    description="A harness is a system used for connecting the rope to the climber. There are two loops at the front of the harness where the climber ties into the rope at the working end using a figure-eight knot. Most harnesses used in climbing are preconstructed and are worn around the pelvis and hips, although other types are used occasionally. Usually young children use a full body harness because it gives more support for the body.",
    categories=category7)
session.add(item2)
session.commit()

# data for Skating
category8 = Categories(name="Skating")
session.add(category8)
session.commit()

item1 = Items(
    name="Roller Skates",
    categories=category8,
    description="Find low prices on adult roller skates and child skates at Skates.com! Shop today and save with free shipping on select skates."
)
session.add(item1)
session.commit()
