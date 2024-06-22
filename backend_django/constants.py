from requests.structures import CaseInsensitiveDict

# mapping for contact form options
purposes = {
    "1": "Editing company pages",
    "2": "Adding your business",
    "3": "Data access",
    "4": "General Inquiry"
}

# P2s linking from dropdown in header
dropdown_content = [
    {
        "name": "Computer Software",
        "link": "/find/computer-software--/"
    },
    {
        "name": "Construction",
        "link": "/find/construction--/"
    },
    {
        "name": "Automotive",
        "link": "/find/automotive--/"
    },
    {
        "name": "Manufacturer",
        "link": "/find/--/?google_industry=Manufacturer"
    },
    {
        "name": "Hospital & Health Care",
        "link": "/find/hospital-&-health-care--/"
    },
    {
        "name": "Financial Services",
        "link": "/find/financial-services--/"
    },
]

# US state abbreviations for dropdown selection in P2
us_state_abbrev = {
'AL': 'Alabama',
 'AK': 'Alaska',
 'AZ': 'Arizona',
 'AR': 'Arkansas',
 'CA': 'California',
 'CO': 'Colorado',
 'CT': 'Connecticut',
 'DE': 'Delaware',
 'DC': 'District of Columbia',
 'FL': 'Florida',
 'GA': 'Georgia',
 'HI': 'Hawaii',
 'ID': 'Idaho',
 'IL': 'Illinois',
 'IN': 'Indiana',
 'IA': 'Iowa',
 'KS': 'Kansas',
 'KY': 'Kentucky',
 'LA': 'Louisiana',
 'ME': 'Maine',
 'MD': 'Maryland',
 'MA': 'Massachusetts',
 'MI': 'Michigan',
 'MN': 'Minnesota',
 'MS': 'Mississippi',
 'MO': 'Missouri',
 'MT': 'Montana',
 'NE': 'Nebraska',
 'NV': 'Nevada',
 'NH': 'New Hampshire',
 'NJ': 'New Jersey',
 'NM': 'New Mexico',
 'NY': 'New York',
 'NC': 'North Carolina',
 'ND': 'North Dakota',
 'OH': 'Ohio',
 'OK': 'Oklahoma',
 'OR': 'Oregon',
 'PA': 'Pennsylvania',
 'RI': 'Rhode Island',
 'SC': 'South Carolina',
 'SD': 'South Dakota',
 'TN': 'Tennessee',
 'TX': 'Texas',
 'UT': 'Utah',
 'VT': 'Vermont',
 'VA': 'Virginia',
 'WA': 'Washington',
 'WV': 'West Virginia',
 'WI': 'Wisconsin',
 'WY': 'Wyoming',
 'Alberta': 'Alberta',
 'British-Columbia': 'British Columbia',
 'Manitoba': 'Manitoba',
 'New-Brunswick': 'New Brunswick',
 'Newfoundland-and-Labrador': 'Newfoundland and Labrador',
 'Northwest-Territories': 'Northwest Territories',
 'Nova-Scotia': 'Nova Scotia',
 'Nunavut': 'Nunavut',
 'Ontario': 'Ontario',
 'Prince-Edward-Island': 'Prince Edward Island',
 'Quebec': 'Quebec',
 'Saskatchewan': 'Saskatchewan',
 'Yukon': 'Yukon'
}

us_state_abbrev = CaseInsensitiveDict(us_state_abbrev)

# Links in the more categories section
links = [
    {
        "name": "New York City",
        "addr": "/find/--NY/?city=New York",
        "imag": "https://www.konaequity.com/static/industries/buildings-2.svg"
    },
    {
        "name": "San Francisco",
        "addr": "/find/--CA/?city=San Francisco",
        "imag": "https://www.konaequity.com/static/industries/monitorz.svg"
    },
    {
        "name": "Real Estate",
        "addr": "/find/real-estate--/",
        "imag": "https://www.konaequity.com/static/industries/building-4.svg"
    },
    {
        "name": "Machinery",
        "addr": "/find/machinery--/",
        "imag": "https://www.konaequity.com/static/industries/car.svg"
    },
    {
        "name": "Fine Art",
        "addr": "/find/fine-art--/",
        "imag": "https://www.konaequity.com/static/industries/brush.svg"
    },
    {
        "name": "Consultant",
        "addr": "/find/?google_industry=Consultant--",
        "imag": "https://www.konaequity.com/static/industries/note.svg"
    },
    {
        "name": "Real Estate Agency",
        "addr": "/find/?google_industry=Real%20estate%20agency--",
        "imag": "https://www.konaequity.com/static/industries/house.svg"
    },
    {
        "name": "Broadcast Media",
        "addr": "/find/Broadcast%20media--",
        "imag": "https://www.konaequity.com/static/industries/text-block.svg"
    },
    {
        "name": "Certified Public Accountant",
        "addr": "/find/?google_industry=Certified%20Public%20Accountant",
        "imag": "https://www.konaequity.com/static/industries/calculator.svg"
    },
    {
        "name": "Helicopter Charter",
        "addr": "/find/?google_industry=Helicopter%20Charter",
        "imag": "https://www.konaequity.com/static/industries/radar-2.svg"
    },
    {
        "name": "Florida",
        "addr": "/find/--FL/",
        "imag": "https://www.konaequity.com/static/industries/format-square.svg"
    },
    {
        "name": "Marketing and Advertising",
        "addr": "/find/marketing-and-advertising--/",
        "imag": "https://www.konaequity.com/static/industries/color-swatch.svg"
    },
]

# Most popular P2 cards displayed in P1
ilinks = [
    {
        "name": "Computer Software",
        "link": "/find/computer-software--/",
        "description": "35k companies",
        "image": "industries/pexcpu2.png"
    },
    {
        "name": "Construction",
        "link": "/find/construction--/",
        "description": "84k companies",
        "image": "industries/pexconstruction.png"
    },
    {
        "name": "Automotive",
        "link": "/find/automotive--/",
        "description": "47k companies",
        "image": "industries/pexauto.png"
    },
    {
        "name": "Manufacturer",
        "link": "/find/--/?google_industry=Manufacturer",
        "description": "39k companies",
        "image": "industries/pexmanufacturer2.png"
    },
    {
        "name": "Hospital and health care",
        "link": "/find/hospital-&-health-care--/",
        "description": "20k companies",
        "image": "industries/pexhospital.png"
    },
    {
        "name": "Insurance Agencies",
        "link": "/find/--/?google_industry=Insurance%2520Agency",
        "description": "33k companies",
        "image": "industries/pexinsurance.png"
    },
]

# Industry mapping for dropdown in P2
industries = {
 'Accounting': 'accounting',
 'Airlines/aviation': 'airlines__aviation',
 'Alternative dispute resolution': 'alternative-dispute-resolution',
 'Alternative medicine': 'alternative-medicine',
 'Animation': 'animation',
 'Apparel & fashion': 'apparel-&-fashion',
 'Architecture & planning': 'architecture-&-planning',
 'Arts and crafts': 'arts-and-crafts',
 'Automotive': 'automotive',
 'Aviation & aerospace': 'aviation-&-aerospace',
 'Banking': 'banking',
 'Biotechnology': 'biotechnology',
 'Broadcast Media': 'broadcast-media',
 'Building materials': 'building-materials',
 'Business supplies and equipment': 'business-supplies-and-equipment',
 'Capital markets': 'capital-markets',
 'Chemicals': 'chemicals',
 'Civic & social organization': 'civic-&-social-organization',
 'Civil engineering': 'civil-engineering',
 'Commercial real estate': 'commercial-real-estate',
 'Computer & network security': 'computer-&-network-security',
 'Computer games': 'computer-games',
 'Computer hardware': 'computer-hardware',
 'Computer networking': 'computer-networking',
 'Computer software': 'computer-software',
 'Construction': 'construction',
 'Consumer electronics': 'consumer-electronics',
 'Consumer Goods': 'consumer-goods',
 'Consumer services': 'consumer-services',
 'Cosmetics': 'cosmetics',
 'Dairy': 'dairy',
 'Defense & space': 'defense-&-space',
 'Design': 'design',
 'Education management': 'education-management',
 'Electrical/electronic manufacturing': 'electrical__electronic-manufacturing',
 'Entertainment': 'entertainment',
 'Environmental services': 'environmental-services',
 'Events services': 'events-services',
 'Executive office': 'executive-office',
 'Facilities services': 'facilities-services',
 'Farming': 'farming',
 'Financial services': 'financial-services',
 'Fine art': 'fine-art',
 'Fishery': 'fishery',
 'Food & beverages': 'food-&-beverages',
 'Food production': 'food-production',
 'Fund-raising': 'fund-raising',
 'Furniture': 'furniture',
 'Gambling & casinos': 'gambling-&-casinos',
 'Glass, ceramics & concrete': 'glass,-ceramics-&-concrete',
 'Government administration': 'government-administration',
 'Government relations': 'government-relations',
 'Graphic design': 'graphic-design',
 'Health, wellness and fitness': 'health,-wellness-and-fitness',
 'Higher education': 'higher-education',
 'Hospital & health care': 'hospital-&-health-care',
 'Hospitality': 'hospitality',
 'Human resources': 'human-resources',
 'Import and export': 'import-and-export',
 'Individual & family services': 'individual-&-family-services',
 'Industrial automation': 'industrial-automation',
 'Information services': 'information-services',
 'Information technology and services': 'information-technology-and-services',
 'Insurance': 'insurance',
 'International affairs': 'international-affairs',
 'International trade and development': 'international-trade-and-development',
 'Internet': 'internet',
 'Investment banking': 'investment-banking',
 'Investment management': 'investment-management',
 'Judiciary': 'judiciary',
 'Law enforcement': 'law-enforcement',
 'Law practice': 'law-practice',
 'Legal services': 'legal-services',
 'Legislative office': 'legislative-office',
 'Leisure, travel & tourism': 'leisure,-travel-&-tourism',
 'Libraries': 'libraries',
 'Logistics and supply chain': 'logistics-and-supply-chain',
 'Luxury goods & jewelry': 'luxury-goods-&-jewelry',
 'Machinery': 'machinery',
 'Management consulting': 'management-consulting',
 'Maritime': 'maritime',
 'Market research': 'market-research',
 'Marketing and advertising': 'marketing-and-advertising',
 'Mechanical or industrial engineering': 'mechanical-or-industrial-engineering',
 'Media Production': 'media-production',
 'Medical devices': 'medical-devices',
 'Medical practice': 'medical-practice',
 'Mental health care': 'mental-health-care',
 'Military': 'military',
 'Mining & metals': 'mining-&-metals',
 'Motion pictures and film': 'motion-pictures-and-film',
 'Museums and institutions': 'museums-and-institutions',
 'Music': 'music',
 'Nanotechnology': 'nanotechnology',
 'Newspapers': 'newspapers',
 'Oil & energy': 'oil-&-energy',
 'Online media': 'online-media',
 'Outsourcing/offshoring': 'outsourcing__offshoring',
 'Package/freight delivery': 'package__freight-delivery',
 'Packaging and containers': 'packaging-and-containers',
 'Paper & forest products': 'paper-&-forest-products',
 'Performing arts': 'performing-arts',
 'Pharmaceuticals': 'pharmaceuticals',
 'Philanthropy': 'philanthropy',
 'Photography': 'photography',
 'Plastics': 'plastics',
 'Political organization': 'political-organization',
 'Primary/secondary education': 'primary__secondary-education',
 'Printing': 'printing',
 'Professional training & coaching': 'professional-training-&-coaching',
 'Program development': 'program-development',
 'Public policy': 'public-policy',
 'Public relations and communications': 'public-relations-and-communications',
 'Public safety': 'public-safety',
 'Publishing': 'publishing',
 'Railroad manufacture': 'railroad-manufacture',
 'Ranching': 'ranching',
 'Real estate': 'real-estate',
 'Recreational facilities and services': 'recreational-facilities-and-services',
 'Religious institutions': 'religious-institutions',
 'Renewables & environment': 'renewables-&-environment',
 'Research': 'research',
 'Restaurants': 'restaurants',
 'Retail': 'retail',
 'Security and investigations': 'security-and-investigations',
 'Semiconductors': 'semiconductors',
 'Shipbuilding': 'shipbuilding',
 'Sporting goods': 'sporting-goods',
 'Sports': 'sports',
 'Staffing and recruiting': 'staffing-and-recruiting',
 'Supermarkets': 'supermarkets',
 'Telecommunications': 'telecommunications',
 'Textiles': 'textiles',
 'Think tanks': 'think-tanks',
 'Tobacco': 'tobacco',
 'Translation and localization': 'translation-and-localization',
 'Transportation/trucking/railroad': 'transportation__trucking__railroad',
 'Utilities': 'utilities',
 'Venture capital & private equity': 'venture-capital-&-private-equity',
 'Veterinary': 'veterinary',
 'Warehousing': 'warehousing',
 'Wholesale': 'wholesale',
 'Wine and spirits': 'wine-and-spirits',
 'Wireless': 'wireless',
 'Writing and editing': 'writing-and-editing'
 }

industries = CaseInsensitiveDict(industries)

# G score descriptions and colors
g_names = ["G1","G2","G3","G4","G5","G6","G7","G8"]
g_descriptions = [
    "Revenue is greater than the industry median.",
    "Income per employee more than industry average.",
    "Revenue growth rate from the first known quarter to current is higher than the industry average.",
    "Employee growth rate from the first known quarter to current is higher than the industry average.",
    "Variance of revenue growth is less than the industry average",
    "Annual revenue growth since founding is higher than the industry average.",
    "Website traffic rankings are better than the industry average",
    "LinkedIn Churn is lower than the industry average."
]
g_colors = ["#00D1C1", "#FF5A5F", "#FFB400", "#007A87", "#FFAA91", "#8CE071"]
g_7_col = ["#00D1C1", "#FF5A5F", "#FFB400", "#FFAA91", "#8CE071", "#F16393", "#DFBEDB"]
g_8_col = ["#00D1C1", "#FF5A5F", "#FFB400", "#FFAA91", "#8CE071", "#F16393", "#DFBEDB", "#007A87"]


# Continents for picture mapping from static directory
continents = {
    'NA': 'North America',
    'SA': 'South America',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}

strong = [
    "{} has a strong market share in their industry",
    "Revenue generated per employee is greater than industry average",
    "Demonstrating revenue growth that is faster than the industry average",
    "The number of employees is growing faster than the industry average",
    "Revenue growth is more steady than the industry average",
    "Since {} was founded, the company has grown faster than the industry average",
    "Web traffic rankings are better than the industry average",
    "Employees are staying with the company and less likely to churn compared to the rest of the industry"
]

weak = [
    "{} has a very small market share in their industry",
    "Revenue generated per employee is less than the industry average",
    "Revenue growth is less than the industry average",
    "The number of employees is not growing as fast as the industry average",
    "Variance of revenue growth is more than the industry average",
    "Since {} was founded, the company has experienced slower revenue growth than the industry average",
    "Web traffic rankings are worse than the industry average",
    "Employees are more likely to churn compared to the industry average",
    "{} will likely have a high level of competition for a deal"
]

def strengthAndWeaknesses(company):
    strengths = []
    weaknesses = []

    if company.g_true == 0:
        strengths.append("There are no known strengths for {}".format(company.name))

    for i in range(1, 9):
        if company.__dict__["g" + str(i)] == True:
            strengths.append(strong[i-1].format(company.name))
        elif company.__dict__["g" + str(i)] == False:
            weaknesses.append(weak[i-1].format(company.name))

    if company.g_true == 8:
        weaknesses.append(company.name + " will likely have a high level of competition for a deal")

    return strengths, weaknesses
