######################################################
# Bob AI Object
#
#
######################################################

# Python Imports

import logging
from openai import OpenAI
from pprint import pprint
import logging, requests, time, json
from pprint import pprint
from pydantic import BaseModel, Field, create_model
from typing import Literal, Optional
from typing import List

from pydantic.fields import FieldInfo
from Controller.Logic.Bob_TokenCost import predict_token_cost

from enum import Enum

from Utils import GlobalVars


class Discipline(str, Enum):
    ARCHITECTURE = "אדריכלות"
    STRUCTURAL_ENGINEERING = "קונסטרוקציה"
    LANDSCAPE_ARCHITECTURE = "אדריכלות נוף"
    USER_SAFETY = "בטיחות המשתמש"
    FIRE_SAFETY = "בטיחות אש"
    HVAC = "מיזוג אויר"
    ELECTRICAL = "חשמל"
    WATER_AND_SEWAGE = "מים וביוב"
    PROTECTION = "מיגון"
    SECURITY = "אבטחה וביטחון"
    TRAFFIC = "תנועה"
    ACCESSIBILITY = "נגישות"
    WATERPROOFING = "איטום"
    ACOUSTICS = "אקוסטיקה"
    SOIL_AND_FOUNDATIONS = "קרקע וביסוס"
    COMMUNICATIONS_AND_IT = "תקשורת ותקשוב"
    INTERIOR_DESIGN = "עיצוב פנים"
    ELEVATORS = "מעליות"
    ENVIRONMENTAL_PROTECTION = "הגנת הסביבה"
    SUSTAINABLE_CONSTRUCTION = "בניה בת קיימה"
    MULTIMEDIA = "מולטימדיה"
    LIGHTING = "תאורה"
    RADIATION = "קרינה"
    THERMAL = "תרמי"
    KITCHENS = "מטבחים"
    MAINTENANCE = "אחזקה"
    HYDROLOGY = "הידרולוגיה"
    LOGISTICS_AND_EQUIPMENT = "לוגיסטיקה והצטיידות"
    CONSERVATION = "שימור"
    SIGNAGE = "שילוט"
    PROGRAMMING = "פרוגרמה"
    GENERAL = "כללי"
    OTHER_NOT_LISTED = "אחר - לא ברשימה"
    LOGISTICS = "לוגיסטיקה"
    COMMUNICATIONS = "תקשורת"

class CommunityFacilityType(str, Enum):
    DAYCARE_CENTER = "מעון יום"
    SCOUT_TRIBE = "שבט צופים"
    COMMUNITY_CENTER = "מרכז קהילתי"
    EARLY_CHILDHOOD_PLAY_CENTER = "משחקיה-מרכז לגיל הרך"
    NEIGHBORHOOD_YOUTH_CLUB = "מועדון נוער שכונתי-מנש"
    SENIOR_CITIZENS_CLUB = "מועדון לאזרחים ותיקים"
    LIBRARY_COMMUNITY_CULTURE_SPORTS = "ספריה-קהילה תרבות וספורט"
    MUSIC_CENTER = "מרכז מוזיקה"
    CULTURE_CENTER = "מרכז תרבות"
    PERFORMANCE_HALL_COMMUNITY_CULTURE_SPORTS = "אולם מופעים-קהילה תרבות וספורט"
    THEATER_COMMUNITY_CULTURE_SPORTS = "תיאטרון-קהילה תרבות וספורט"
    MUSEUM_ART_GALLERY = "מוזיאון-גלרייה לאמנות"
    COMMUNITY_COUNTRY_CLUB = "קאנטרי קהילתי"
    SWIMMING_POOL = "בריכת שחייה"
    FOOTBALL_FIELD_COMMUNITY_CULTURE_SPORTS = "מגרש כדורגל-קהילה תרבות וספורט"
    SPORTS_FIELDS_AND_ATHLETICS_FACILITIES = "מגרשי ספורט ומתקני אתלטיקה-קהילה תרבות וספורט"
    TENNIS_CENTER = "מרכז טניס"
    SPORTS_HALL_COMMUNITY_CULTURE_SPORTS = "אולם ספורט-קהילה, תרבות וספורט"
    OUTDOOR_FITNESS_FACILITIES = "מתקני כושר חיצוניים-קהילה תרבות וספורט"
    OTHER_COMMUNITY_CULTURE_SPORTS = "תרבות קהילה וספורט-נוספים"

from enum import Enum


from enum import Enum


class EducationalFacilityType(str, Enum):
    DAYCARE_CENTER = "מעון יום"
    SPECIAL_EDUCATION_DAYCARE = "מעון יום חינוך מיוחד"
    PRIVATE_DAYCARE = "מעון יום פרטי"
    GOVERNMENT_SUPERVISED_DAYCARE = "מעון יום בפיקוח ממשלתי"

    KINDERGARTEN_CLUSTER = "אשכול גני ילדים"
    KINDERGARTEN = "גן ילדים"

    PRIMARY_SCHOOL = "בית ספר יסודי"
    SPECIAL_EDUCATION_PRIMARY_SCHOOL = "בית ספר יסודי חינוך מיוחד"

    SECONDARY_SCHOOL = "בית ספר על יסודי"
    SPECIAL_EDUCATION_SECONDARY_SCHOOL = "בית ספר על יסודי חינוך מיוחד"

    EDUCATIONAL_SPORTS_HALL = "אולם ספורט-חינוך"
    EDUCATIONAL_SPORTS_FIELDS_AND_ATHLETICS = "מגרשי ספורט ומתקני אתלטיקה-חינוך"
    EDUCATIONAL_OUTDOOR_FITNESS_FACILITIES = "מתקני כושר חיצוניים-חינוך"


class EducationalFacilitySpaceType(str, Enum):
    # =========================
    # Secondary School (על יסודי)
    # =========================
    SECONDARY_SCHOOL_GENERAL_STRUCTURE_AND_SYSTEMS = "כלל המבנה ומערכות בית ספר על יסודי"
    SECONDARY_SCHOOL_ENTRANCES_GATES_FENCING_GUARD_BOOTH = "כניסות-שערים-גידור-ביתן שומר בבית ספר על יסודי"
    SECONDARY_SCHOOL_BICYCLE_PARKING = "חניית אופניים בבית ספר על יסודי"
    SECONDARY_SCHOOL_VEHICLE_PARKING = "חניית כלי רכב בבית ספר על יסודי"
    SECONDARY_SCHOOL_YARD_GARDEN = "חצר-גינה בבית ספר על יסודי"
    SECONDARY_SCHOOL_SPORTS_FIELDS_AND_SHADED_FACILITIES = "מגרשים ומתקני ספורט-הצללות בבית ספר על יסודי"
    SECONDARY_SCHOOL_SPORTS_HALL = "אולם ספורט בבית ספר על יסודי"
    SECONDARY_SCHOOL_MAIN_LOBBY = "מבואה ראשית בבית ספר על יסודי"
    SECONDARY_SCHOOL_CORRIDOR = "מסדרון בבית ספר על יסודי"
    SECONDARY_SCHOOL_OUTDOOR_CLASSROOM = "חלל חוץ כיתתי ללמידה בבית ספר על יסודי"
    SECONDARY_SCHOOL_CAFETERIA_SNACK_BAR = "קפיטריה-מזנון בבית ספר על יסודי"
    SECONDARY_SCHOOL_AUDITORIUM = "אודיטוריום בבית ספר על יסודי"

    # Administration – Secondary School
    SECONDARY_SCHOOL_PRINCIPAL_OFFICE = "משרד מנהל/ת בבית ספר על יסודי"
    SECONDARY_SCHOOL_VICE_PRINCIPAL_OFFICE = "משרד ס. מנהל/ת בבית ספר על יסודי"
    SECONDARY_SCHOOL_PRINCIPAL_SECRETARIAT = "מזכירות מנהל בבית ספר על יסודי"
    SECONDARY_SCHOOL_STUDENT_SECRETARIAT = "מזכירות תלמידים/ות בבית ספר על יסודי"
    SECONDARY_SCHOOL_MEETING_ROOM = "חדר ישיבות בבית ספר על יסודי"
    SECONDARY_SCHOOL_ACCOUNTING = "הנהלת חשבונות בבית ספר על יסודי"
    SECONDARY_SCHOOL_ARCHIVE = "ארכיב בבית ספר על יסודי"

    # Staff – Secondary School
    SECONDARY_SCHOOL_TEACHERS_ROOM_AND_KITCHENETTE = "חדר מורים/ות ומטבחון בבית ספר על יסודי"
    SECONDARY_SCHOOL_STAFF_ROOMS = "חדרי סגל בבית ספר על יסודי"
    SECONDARY_SCHOOL_TEACHER_LOUNGE = "חדר שהייה למורה בבית ספר על יסודי"
    SECONDARY_SCHOOL_FLOOR_TEACHERS_LOUNGES = "פינות שהייה-חדר מורים/ות קומתי בבית ספר על יסודי"

    # Learning – Secondary School
    SECONDARY_SCHOOL_LIBRARY_AND_READING_ROOM = "ספרייה-חדר עיון בבית ספר על יסודי"
    SECONDARY_SCHOOL_CLASSROOM = "כיתת לימוד בבית ספר על יסודי"
    SECONDARY_SCHOOL_SPECIAL_EDUCATION_CLASSROOM = "כיתת לימוד חינוך מיוחד בבית ספר על יסודי"
    SECONDARY_SCHOOL_SUPPORT_ROOM = "חדר עזר בבית ספר על יסודי"
    SECONDARY_SCHOOL_INDIVIDUAL_WORK_ROOM = "חדר עבודה פרטנית בבית ספר על יסודי"
    SECONDARY_SCHOOL_GRADE_COORDINATORS_ROOM = "חדר רכזי שכבות בבית ספר על יסודי"
    SECONDARY_SCHOOL_STUDENT_COUNCIL_ROOM = "חדר מועצת תלמידים/ות בבית ספר על יסודי"
    SECONDARY_SCHOOL_PARENT_MEETING_ROOM = "חדר קבלת הורים בבית ספר על יסודי"
    SECONDARY_SCHOOL_INNOVATION_ROOM = "חדר יזמות בבית ספר על יסודי"
    SECONDARY_SCHOOL_COMPUTER_ROOM = "חדר מחשבים בבית ספר על יסודי"
    SECONDARY_SCHOOL_IT_SERVICES = "שירות מחשבים בבית ספר על יסודי"

    # Labs – Secondary School
    SECONDARY_SCHOOL_PHYSICS_LAB = "מעבדות מדעים-פיזיקה-בבית ספר על יסודי"
    SECONDARY_SCHOOL_CHEMISTRY_LAB = "מעבדות מדעים-כימיה-בבית ספר על יסודי"
    SECONDARY_SCHOOL_BIOLOGY_LAB = "מעבדות מדעים-ביולוגיה-בבית ספר על יסודי"
    SECONDARY_SCHOOL_LABS_LOGISTICS_CENTER = "מוקד לוגיסטי מעבדות בבית ספר על יסודי"
    SECONDARY_SCHOOL_HAZARDOUS_MATERIALS_ROOM = "חדר חומרים מסוכנים מעבדות בבית ספר על יסודי"

    # Support – Secondary School
    SECONDARY_SCHOOL_TECHNOLOGY_AND_ART_ROOMS = "חדרי טכנולוגיה-ספח אומנות בבית ספר על יסודי"
    SECONDARY_SCHOOL_COMMUNICATION_ROOM = "חדר תקשורת בבית ספר על יסודי"
    SECONDARY_SCHOOL_NURSE_ROOM = "חדר אח/ות בבית ספר על יסודי"
    SECONDARY_SCHOOL_COUNSELOR_ROOM = "חדר יועץ/ת בבית ספר על יסודי"
    SECONDARY_SCHOOL_ART_THERAPY_ROOM = "חדר טיפול באמנויות בבית ספר על יסודי"
    SECONDARY_SCHOOL_PSYCHOLOGY_AND_OCCUPATIONAL_THERAPY = "חדר פסיכולוגיה-ריפוי בעיסוק בבית ספר על יסודי"
    SECONDARY_SCHOOL_SPECIAL_ED_TEAM_SPACE = "מרחב צוות חינוך מיוחד בבית ספר על יסודי"
    SECONDARY_SCHOOL_CUSTODIAN_ROOM = "חדר אב/ם בית בבית ספר על יסודי"
    SECONDARY_SCHOOL_STORAGE_ROOMS = "מחסנים בבית ספר על יסודי"
    SECONDARY_SCHOOL_CLEANING_ROOM = "חדר ניקיון בבית ספר על יסודי"
    SECONDARY_SCHOOL_RESTROOMS = "שירותים בבית ספר על יסודי"
    SECONDARY_SCHOOL_PROTECTED_SPACES = "מרחבים מוגנים בבית ספר על יסודי"
    SECONDARY_SCHOOL_WASTE_ROOM = "חדר אשפה בבית ספר על יסודי"
    SECONDARY_SCHOOL_RECYCLING_FACILITIES = "מתקני מחזור בבית ספר על יסודי"

    # =========================
    # Primary School (יסודי)
    # =========================
    PRIMARY_SCHOOL_GENERAL_STRUCTURE_AND_SYSTEMS = "כלל המבנה ומערכות בית ספר יסודי"
    PRIMARY_SCHOOL_NEIGHBORHOOD_FRONTAGE = "עם הפנים לשכונה בבית ספר יסודי"
    PRIMARY_SCHOOL_BICYCLE_PARKING = "חניית אופניים בבית ספר יסודי"
    PRIMARY_SCHOOL_PLAYGROUND = "חצר משחק בבית ספר יסודי"
    PRIMARY_SCHOOL_LEARNING_GARDEN = "גינה לימודית בבית ספר יסודי"
    PRIMARY_SCHOOL_SPORTS_FIELDS_AND_SHADED_FACILITIES = "מגרשים ומתקני ספורט-הצללות בבית ספר יסודי"
    PRIMARY_SCHOOL_SPORTS_HALL = "אולם ספורט בבית ספר יסודי"
    PRIMARY_SCHOOL_MAIN_LOBBY = "מבואה ראשית בבית ספר יסודי"
    PRIMARY_SCHOOL_OUTDOOR_LEARNING_AND_CORRIDORS = "חלל חוץ כיתתי ללמידה ומסדרונות בבית ספר יסודי"

    PRIMARY_SCHOOL_PRINCIPAL_OFFICE = "משרד מנהל/ת בבית ספר יסודי"
    PRIMARY_SCHOOL_VICE_PRINCIPAL_OFFICE = "משרד ס. מנהל/ת בבית ספר יסודי"
    PRIMARY_SCHOOL_SECRETARIAT = "מזכירות בבית ספר יסודי"
    PRIMARY_SCHOOL_TEACHERS_ROOM_AND_KITCHENETTE = "חדר מורים/ות ומטבחון בבית ספר יסודי"
    PRIMARY_SCHOOL_LIBRARY_AND_READING_ROOM = "ספרייה-חדר עיון בבית ספר יסודי"
    PRIMARY_SCHOOL_MULTIPURPOSE_HALL = "אולם רב תכליתי בבית ספר יסודי"

    PRIMARY_SCHOOL_PROJECTS_ROOM = "חדר פרוייקטים בבית ספר יסודי"
    PRIMARY_SCHOOL_INNOVATION_ROOM = "חדר יזמות בבית ספר יסודי"
    PRIMARY_SCHOOL_CLASSROOM = "כיתת לימוד בבית ספר יסודי"
    PRIMARY_SCHOOL_SPECIAL_EDUCATION_CLASSROOM = "כיתת לימוד חינוך מיוחד בבית ספר יסודי"
    PRIMARY_SCHOOL_SPECIAL_EDUCATION_SUPPORT_ROOM = "חדר עזר חינוך מיוחד בבית ספר יסודי"
    PRIMARY_SCHOOL_INDIVIDUAL_WORK_ROOM = "חדר עבודה פרטנית בבית ספר יסודי"
    PRIMARY_SCHOOL_GROUPING_SUPPORT_ROOM = "חדר עזר הקבצות בבית ספר יסודי"
    PRIMARY_SCHOOL_TECHNOLOGY_ROOM = "חדר טכנולוגיה בבית ספר יסודי"
    PRIMARY_SCHOOL_SCIENCE_ROOM = "חדר מדעים בבית ספר יסודי"
    PRIMARY_SCHOOL_SCIENCE_PREP_ROOM = "חדר הכנה למדעים בבית ספר יסודי"

    PRIMARY_SCHOOL_NURSE_ROOM = "חדר אח/ות בבית ספר יסודי"
    PRIMARY_SCHOOL_COUNSELOR_ROOM = "חדר יועץ/ת בבית ספר יסודי"
    PRIMARY_SCHOOL_SPECIAL_EDUCATION_THERAPY_ROOM = "חדר טיפול לחינוך מיוחד בבית ספר יסודי"
    PRIMARY_SCHOOL_SPECIAL_ED_TEAM_SPACE = "מרחב צוות חינוך מיוחד בבית ספר יסודי"
    PRIMARY_SCHOOL_CUSTODIAN_ROOM = "חדר אב/ם בית בבית ספר יסודי"
    PRIMARY_SCHOOL_STORAGE_ROOMS = "מחסנים בבית ספר יסודי"
    PRIMARY_SCHOOL_PROTECTED_SPACES = "מרחבים מוגנים בבית ספר יסודי"
    PRIMARY_SCHOOL_COMMUNICATION_ROOM = "חדר תקשורת בבית ספר יסודי"
    PRIMARY_SCHOOL_CLEANING_ROOM = "חדר ניקיון בבית ספר יסודי"
    PRIMARY_SCHOOL_RESTROOMS = "שירותים בבית ספר יסודי"
    PRIMARY_SCHOOL_WASTE_ROOM = "חדר אשפה בבית ספר יסודי"
    PRIMARY_SCHOOL_RECYCLING_FACILITIES = "מתקני מחזור בבית ספר יסודי"

    # ==========================================
    # Kindergarten & Daycare Cluster (אשכול גנים)
    # ==========================================
    KINDERGARTEN_CLUSTER_GENERAL_STRUCTURE_AND_SYSTEMS = "כלל המבנה ומערכות אשכול גני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_ENTRANCES_GATES_FENCING_GUARD_BOOTH = "כניסות-שערים-גידור-ביתן שומר בגני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_BICYCLE_PARKING = "חניית אופניים בגני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_STROLLER_PARKING = "חניית עגלות פעוטות בגני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_PRINCIPAL_OFFICE = "משרד מנהל/ת באשכול גני ילדים"

    KINDERGARTEN_CLASSROOM = "כיתה בגן ילדים"
    DAYCARE_CLASSROOM = "כיתה במעונות יום"
    KINDERGARTEN_CLUSTER_CLASSROOM_KITCHENETTE = "מטבחון כיתתי בגני ילדים ומעונות יום"
    KINDERGARTEN_RESTROOMS = "שירותים בגן ילדים"
    DAYCARE_RESTROOMS = "שירותים במעונות יום"
    KINDERGARTEN_CLUSTER_STORAGE = "מחסן בגני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_PROTECTED_SPACES = "מרחבים מוגנים בגני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_PLAYGROUND_GARDEN = "מרפסת-חצר משחק-גינה בגני ילדים ומעונות יום"

    KINDERGARTEN_CLUSTER_MULTIPURPOSE_ACTIVITY_ROOM = "חדר פעילות רב תחומי באשכול גני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_ART_SCIENCE_COMPUTERS_ROOM = "חדר אמנות-מדעים-מחשבים באשכול גני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_MOVEMENT_AND_GYMBORIE_ROOM = "חדר תנועה-ג'ימבורי באשכול גני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_COOKING_AND_WARMING_KITCHEN = "מטבח מבשל-מחמם באשכול גני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_LAUNDRY_ROOM = "חדר כביסה בגני ילדים ומעונות יום"
    KINDERGARTEN_CLUSTER_WASTE_ROOM = "חדר אשפה בגני ילדים ומעונות יום"


class FacilitySpaceType(str, Enum):
    # Community Center – General
    COMMUNITY_CENTER_GENERAL_STRUCTURE_AND_SYSTEMS = "כלל המבנה ומערכות מרכז קהילתי"
    COMMUNITY_CENTER_ENTRANCES_GATES_FENCING = "כניסות-שערים-גידור במרכז קהילתי"
    COMMUNITY_CENTER_MAIN_LOBBY_URBAN_LIVING_ROOM = "סלון עירוני-מבואה ראשית במרכז קהילתי"
    COMMUNITY_CENTER_RESTAURANT_CAFE_SNACK_BAR = "מסעדה-בית קפה-מזנון במרכז קהילתי"
    COMMUNITY_CENTER_RECEPTION_AND_SECRETARIAT = "קבלה ומזכירות במרכז קהילתי"
    COMMUNITY_CENTER_DIRECTOR_OFFICE = "משרד מנהל.ת במרכז קהילתי"
    COMMUNITY_CENTER_STAFF_MEETING_ROOM = "חדר ישיבות צוות במרכז קהילתי"
    COMMUNITY_CENTER_STAFF_KITCHENETTE = "מטבחון צוות במרכז קהילתי"
    COMMUNITY_CENTER_STAFF_OFFICES = "משרדי צוות במרכז קהילתי"
    COMMUNITY_CENTER_PROTECTED_SPACES = "מרחבים מוגנים במרכז קהילתי"
    COMMUNITY_CENTER_RESTROOMS = "שירותים במרכז קהילתי"
    COMMUNITY_CENTER_STORAGE_ROOMS = "מחסנים במרכז קהילתי"
    COMMUNITY_CENTER_MULTIPURPOSE_ASSEMBLY_AND_PERFORMANCE_HALL = "אולם התכנסויות ומופעים רב תכליתי במרכז קהילתי"
    COMMUNITY_INDEPENDENT_MULTIPURPOSE_HALL = "אולם התכנסויות ומופעים רב תכליתי קהילתי עצמאי"

    # Libraries
    COMMUNITY_CENTER_LIBRARY = "ספרייה במרכז קהילתי"
    INDEPENDENT_COMMUNITY_LIBRARY = "ספרייה קהילתית עצמאית"
    COMMUNITY_CENTER_OBJECT_LENDING_LIBRARY = "תל קח-ספריית השאלת חפצים במרכז קהילתי"

    # Community Uses
    SENIOR_CITIZENS_CLUB = "מועדון לאזרחים ותיקים"
    COMMUNITY_COWORKING_SPACE = "מרחב עבודה משותף קהילתי"
    NEIGHBORHOOD_YOUTH_CENTER = "מרכז נוער שכונתי-מנש"
    EARLY_CHILDHOOD_PLAY_CENTER = "משחקיה-מרכז לגיל הרך"

    # Activity & Learning Spaces
    COMMUNITY_CENTER_ART_ROOM_WITH_KILN = "חדר אמנות (כולל תנור קרמיקה ומחסן) במרכז קהילתי"
    COMMUNITY_CENTER_ACTIVITY_CLASSROOM = "כיתת פעילות-לימוד-חדר חוגים במרכז קהילתי"
    COMMUNITY_CENTER_CREATORS_AND_MAKERS_WORKSHOPS = "סדנאות יצירה-מייקרים במרכז קהילתי"
    COMMUNITY_CENTER_TECHNOLOGY_CENTER = "תיק-טק-מרכז טכנולוגי במרכז קהילתי"
    COMMUNITY_CENTER_MUSIC_AND_RECORDING_ROOMS = "חדרי מוזיקה-הקלטות-סאונד במרכז קהילתי"
    COMMUNITY_CENTER_COMMUNITY_KITCHEN_COOKING_CLASSES = "מטבח קהילתי-חדר חוגי בישול במרכז קהילתי"

    # Sports & Wellness – Community Center
    COMMUNITY_CENTER_MULTIPURPOSE_TRAINING_STUDIO = "סטודיו אימונים רב תכליתי במרכז קהילתי"
    COMMUNITY_CENTER_DANCE_STUDIO = "סטודיו למחול במרכז קהילתי"
    COMMUNITY_CENTER_MARTIAL_ARTS_STUDIO = "סטודיו לאמנויות לחימה במרכז קהילתי"
    COMMUNITY_CENTER_GYM = "חדר כושר במרכז קהילתי"
    COMMUNITY_CENTER_OUTDOOR_FITNESS_FACILITIES = "מתקני כושר חיצוניים במרכז קהילתי"
    COMMUNITY_CENTER_STUDIO_CHANGING_ROOM = "חדר הלבשה צמוד לסטודיו במרכז קהילתי"
    COMMUNITY_CENTER_LOCKER_ROOMS_AND_SHOWERS = "חדרי הלבשה ורחצה במרכז קהילתי"

    # Service & Support – Community Center
    FIRST_AID_ROOM = "חדר עזרה ראשונה"
    COMMUNITY_CENTER_CLEANING_ROOM = "חדר ניקיון במרכז קהילתי"
    COMMUNITY_CENTER_WASTE_ROOM = "חדר אשפה במרכז קהילתי"
    COMMUNITY_CENTER_IT_COMMUNICATION_ROOM = "חדר תקשורת מחשב במרכז קהילתי"
    COMMUNITY_CENTER_BICYCLE_PARKING = "חניית אופניים במרכז קהילתי"
    COMMUNITY_CENTER_STROLLER_PARKING = "חניית עגלות פעוטות במרכז קהילתי"
    COMMUNITY_CENTER_PLAYGROUND_YARD = "חצר משחק במרכז קהילתי"

    # Community Country Club – General
    COMMUNITY_COUNTRY_CLUB_GENERAL_STRUCTURE_AND_SYSTEMS = "כלל המבנה ומערכות קאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_ENTRANCES_GATES_FENCING = "כניסות-שערים-גידור בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_RECEPTION_AND_SECRETARIAT = "קבלה ומזכירות בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_DIRECTOR_OFFICE = "משרד מנהל.ת בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_STAFF_MEETING_ROOM = "חדר ישיבות צוות בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_STAFF_KITCHENETTE = "מטבחון צוות בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_STAFF_OFFICES = "משרדי צוות בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_PROTECTED_SPACES = "מרחבים מוגנים בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_RESTROOMS = "שירותים בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_STORAGE_ROOMS = "מחסנים בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_MACHINE_ROOM = "חדר מכונות בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_ACTIVE_ROOF = "גג פעיל בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_BICYCLE_PARKING = "חניית אופניים בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_STROLLER_PARKING = "חניית עגלות פעוטות בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_RESTAURANT_CAFE_SNACK_BAR = "מסעדה-בית קפה-מזנון בקאנטרי קהילתי"

    # Gym – Country Club
    COMMUNITY_COUNTRY_CLUB_GYM_COMPLEX = "חדר כושר-כלל המכלול-בקאנטרי קהילתי"
    GYM_CARDIO_EQUIPMENT = "חדר כושר-מכשירים (הליכונים-אליפטיים-מדרגות)"
    GYM_WEIGHT_MACHINES = "חדר כושר-מכשירי משקולות"
    GYM_FREE_WEIGHTS = "חדר כושר-משקולות חופשיים"
    GYM_FUNCTIONAL_TRAINING = "חדר כושר-אימון פונקציונאלי"
    GYM_BOXING_RING_AND_BAGS = "חדר כושר-זירת אגרוף ושקים"

    # Spa & Pools
    COMMUNITY_COUNTRY_CLUB_SPA_SAUNAS_JACUZZI = "ספא-סאונות-ג'קוזי בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_LOCKER_ROOMS_AND_SHOWERS = "חדרי הלבשה ורחצה בקאנטרי קהילתי"
    OUTDOOR_SUMMER_LEARNING_POOL = "בריכה לימודית חיצונית-קיצית בקאנטרי קהילתי"
    INDOOR_SWIMMING_POOL = "בריכת שחיה מקורה בקאנטרי קהילתי"
    OUTDOOR_SUMMER_TODDLER_POOL = "בריכת פעוטות חיצונית-קיצית בקאנטרי קהילתי"
    INDOOR_TODDLER_POOL = "בריכת פעוטות מקורה בקאנטרי קהילתי"
    INDOOR_LEARNING_POOL = "בריכה לימודית מקורה בקאנטרי קהילתי"
    INDOOR_THERAPEUTIC_POOL = "בריכה טיפולית מקורה בקאנטרי קהילתי"

    # Studios – Country Club
    SPINNING_BIKE_ROOM = "חדר אופני ספינינג בקאנטרי קהילתי"
    YOGA_ROOM = "חדר יוגה בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_MULTIPURPOSE_TRAINING_STUDIO = "סטודיו אימונים רב תכליתי בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_DANCE_STUDIO = "סטודיו למחול בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_MARTIAL_ARTS_STUDIO = "סטודיו לאמנויות לחימה בקאנטרי קהילתי"
    COMMUNITY_COUNTRY_CLUB_TENNIS_COURTS = "מגרשי טניס בקאנטרי קהילתי"

    # Scout Tribe
    SCOUT_TRIBE_GENERAL_STRUCTURE_AND_SYSTEMS = "כלל המבנה ומערכות שבט צופים"
    SCOUT_TRIBE_ENTRANCES_GATES_FENCING = "כניסות-שערים-גידור בשבט צופים"
    SCOUT_TRIBE_BICYCLE_PARKING = "חניית אופניים בשבט צופים"
    SCOUT_TRIBE_ASSEMBLY_FIELD = "מגרש מסדרים בשבט צופים"
    SCOUT_TRIBE_MEMORIAL_CORNER = "פינת זיכרון בשבט צופים"
    SCOUT_TRIBE_ACTIVITY_AREA = "שטח לפעילות צופית בשבט צופים"
    SCOUT_TRIBE_WOODWORK_FACILITY = "מתקן סנדות עץ בשבט צופים"
    SCOUT_TRIBE_LARGE_HALL = "אולם גדול בשבט צופים"
    SCOUT_TRIBE_ACTIVITY_ROOMS = "חדרי פעילות בשבט צופים"
    SCOUT_TRIBE_SENIOR_YOUTH_ROOM = "חדר שכבג בשבט צופים"
    SCOUT_TRIBE_GUIDANCE_ROOM = "חדר הדרכה בשבט צופים"
    SCOUT_TRIBE_COORDINATORS_ROOM = "חדר רכזים בשבט צופים"
    SCOUT_TRIBE_GENERAL_STORAGE = "מחסן כללי בשבט צופים"
    SCOUT_TRIBE_SUMMER_STORAGE = "מחסן קיץ בשבט צופים"
    SCOUT_TRIBE_KIOSK = "קיוסק בשבט צופים"
    SCOUT_TRIBE_RESTROOMS = "שירותים בשבט צופים"
    SCOUT_TRIBE_WASTE_ROOM = "חדר אשפה בשבט צופים"

    # Other
    OTHER_NOT_LISTED = "אחר-לא ברשימה"


class BobAIModel_CorrectTextAndGetSection(BaseModel):
    """
    Book Best Results
    """
    corrected_text: str
    section_number: str

class ClassificationResultEducation(BaseModel):
    facility_types: List[EducationalFacilityType] = Field(
        description="Relevant high-level education facility types"
    )
    facility_space_types: List[EducationalFacilitySpaceType] = Field(
        description="Relevant specific spaces or areas"
    )
    disciplines: List[Discipline] = Field(
        description="Relevant professional disciplines"
    )

class ClassificationResultCommunity(BaseModel):
    facility_types: List[CommunityFacilityType] = Field(
        description="Relevant high-level community facility types"
    )
    facility_space_types: List[FacilitySpaceType] = Field(
        description="Relevant specific spaces or areas"
    )
    disciplines: List[Discipline] = Field(
        description="Relevant professional disciplines"
    )

class TextBlock(BaseModel):
    text: str   # The actual text content
    section_number: str = None
    is_guideline_text: bool

class ImageParseResult(BaseModel):
    blocks: List[TextBlock]


######################## Bob AI Object #####################

class Bob_AI_Object:

    """
    Bob AI Object
    """

    ########################## Inits #######################

    def __init__(self):
        """
        Inits
        """
        #logging.debug('Initializing BOB AI Object ..')
        self._headers = {'Content-Type': 'application/json; charset=utf-8',
                         'x-secret': 'bobbyisusingaiandlovesit'}
        self._timeout = 60
        self._client = OpenAI(api_key=GlobalVars.prop_openai_api_key)

    ########################## Fires Request #######################

    def __fire_request(self, route, data, is_get=False, look_for_failed_text=False):
        """
        Fire Request
        """
        _now = time.time()
        _url = self.EMBEDDINGS_SERVER_URL.format(route)
        try:
            if is_get is False:
                _result = requests.post(_url, headers=self._headers,
                                        json=data, timeout=self._timeout)
            else:
                _result = requests.get(_url, headers=self._headers,
                                       params=data, timeout=self._timeout)
        except requests.exceptions.Timeout:
            logging.error('Request Timed Out -> Will sleep ..')
            return None, -1, {}
        if _result.status_code != 200:
            logging.error('Exception in AI Request: {}'.format(route))
            print(_result.status_code)
            return None, -1, {}
        elif look_for_failed_text is True:
            if _result.text.lower().find('error') != -1 or _result.text.lower().find('fail') != -1:
                print(_result.text)
                logging.error('Error/Failure in AI Request: {} / {}'.format(route, data))
                input("<Paused>")
                return None, -1, {}
        _took_time = round((time.time() - _now), 4)
        return _result.text, _took_time, _result.json()

    ########################## Print Cost ##########################

    def _print_cost(self, result):
        """
        Print Cost
        :param result:
        :return:
        """
        usage = result.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens

        input_cost = (prompt_tokens / 1000) * 0.005  # $0.005 per 1K input tokens
        output_cost = (completion_tokens / 1000) * 0.015  # $0.015 per 1K output tokens
        total_cost = input_cost + output_cost

        print(prompt_tokens, completion_tokens)

        #print(f"Input: {prompt_tokens} tokens | Output: {completion_tokens} tokens")
        #print(f"Cost: ${input_cost:.6f} input + ${output_cost:.6f} output = ${total_cost:.6f}")

    ######################## Correct Text And Get Index Number ##########################

    def correct_text_and_get_section_number(self, text):
        """
        Debug
        """
        _model = 'gpt-5.2'
        _messages = [
            {"role": "system", "content": (
    "You are an automated Hebrew document restoration and parsing system. "
    "You receive raw text extracted from a badly generated PDF. "
    "The text may be corrupted, reversed, fragmented, incorrectly ordered, "
    "or contain mixed RTL/LTR issues.\n\n"

    "Your tasks are:\n"
    "1. Restore the text into correct, fluent Hebrew.\n"
    "2. Identify and extract the section number if it exists.\n"
    "3. Remove the section number from the restored text.\n\n"

    "Section number formats may include:\n"
    "- x.\n"
    "- x.x.\n"
    "- x.x.x\n"
    "- x.x.x.x\n\n"

    "Important rules:\n"
    "- Preserve the original meaning exactly.\n"
    "- Do NOT summarize, interpret, or add new content.\n"
    "- Do NOT include the section number inside the corrected text.\n"
    "- If no section number is explicitly present, return null for the section number.\n"
    "- Keep the output clean, professional, and in fluent Hebrew.\n"
    "- Do NOT include explanations or reasoning.\n\n"

    "Return the result strictly according to the required response schema."
) },

            {"role": "user", "content": 'text: {}'.format(text)}

        ]
        _result = self._client.beta.chat.completions.parse(
            model=_model,
            messages=_messages,
            response_format=BobAIModel_CorrectTextAndGetSection,
            temperature=0,
            timeout=300,
        )
        _json = json.loads(_result.choices[0].message.content)
        return _json

    ######################## Match Discipline To Guide Line ##########################

    def classify_guideline(self, major_headline, headline_a, headline_b, guideline_text, name):
        """
        Debug
        """
        _model = 'gpt-4o-mini'
        SYSTEM_PROMPT =  """
        You are a professional classifier for municipal, architectural, and community projects.

        Given a major_headline, headline_a, headline_b, guideline_text:
        1. Identify the relevant COMMUNITY FACILITY TYPES
        2. Identify the relevant FACILITY SPACE TYPES
        3. Identify the relevant DISCIPLINES

        Rules:
        - Each category may contain MULTIPLE values
        - Return ONLY valid JSON
        - Use ONLY values that exist in the provided enums
        - If nothing matches, use OTHER_NOT_LISTED
        """
        _format = None
        if name == 'education' or name =='yazamim':
            _format = ClassificationResultEducation
        if name == 'community':
            _format = ClassificationResultCommunity
        _messages = [
            {"role": "system", "content": SYSTEM_PROMPT },

            {"role": "user", "content": 'major_headline: {}\nheadline_a:{}\nheadline_b:{}\nguideline_text:{}'
            .format(major_headline, headline_a, headline_b, guideline_text)},

        ]
        _result = self._client.beta.chat.completions.parse(
            model=_model,
            messages=_messages,
            response_format=_format,
            temperature=1,
        )
        #a = predict_token_cost(_messages, _format, model='gpt-4o-mini')
        #print(a['total_cost_usd'])
        _json = json.loads(_result.choices[0].message.content)
        #self._print_cost(_result)
        return _json
        #return None

    ######################## Get Page Structure And Text From Base64 Image ##########################

    def get_page_structure_and_text_from_base64_image(self, base64_image):
        """
        Debug
        """
        _model = 'gpt-5.2'
        image_data_url = f"data:image/png;base64,{base64_image}"
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert document parser specializing in extracting text and hierarchical structure from images.\n\n"
                    "Your tasks:\n"
                    "1. Extract ALL text visible in the image exactly as it appears (original_text).\n"
                    "2. Relate each piece of text, to its corresponding section number"
                    "3. Preserve entirely the text block as it is appearing in the image -> except for section_number if appearing inside it. "
                    "4. is_guideline_text : should be True if the section_number is the most 'bottom' in the hierarchy of this page"
                    "3. Ignore tables."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please extract the text and hierarchy from this image:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url,
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
        _result = self._client.beta.chat.completions.parse(
            model=_model,
            messages=messages,
            response_format=ImageParseResult,
            temperature=0)
        _json = json.loads(_result.choices[0].message.content)
        return _json


