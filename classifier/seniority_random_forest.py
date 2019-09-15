from joblib import dump, load
from parsers.education_parser import time_since_last_education, get_proxy_for_degree
from parsers.experience_parser import get_longest_tenure
from configs import MODEL_PATH

SAMPLE_PROFILES = [{"seniority_level": "Mid-Level", "education": [{"school": "University of Wisconsin Madison", "description": "University of Wisconsin - Madison   Madison, WI\n\nSeptember 2005 - December 2009\nBachelor of Business Administration, Marketing, GPA 3.5/4.0", "degree": "Bachelor of Business Administration", "time": ["2005-09-01", "2009-12-01"]}, {"school": "UW", "description": "Certificate in Spanish Studies\nDean's List - Fall 2005\nUW Real Estate Club (4 Semesters)", "degree": "Certificate in Spanish", "time": ["notKnown", "2005-09-01"]}, {"school": "Universidad de Sevilla", "description": "Business Action for Sustainable Enterprise, B.A.S.E. (6 Semesters)\n\nUniversidad de Sevilla   Sevilla, Spain\nApril 2007 - December 2007", "degree": "B.A.S.E.", "time": ["2007-04-01", "2007-12-01"]}, {"school": "American TESOL Institute", "description": "American TESOL Institute   Phuket, Thailand\nApril 2010\nIntense 3-week teaching course\nInternationally recognized TEFL certificate, with a practical emphasis on teaching skills, cultural training, language awareness, phonology and classroom management", "degree": "certificate", "time": ["notKnown", "2010-04-01"]}], "experience": [{"skills": ["marketing", "campaigns", "management", "marketing automation", "roi", "salesforce.com", "direct mail", "analytics", "analysis", "strategy", "metrics", "campaign effectiveness", "webinars", "creative development", "online", "selection", "foundation", "dinners", "engagement", "lead scoring"], "time": ["2014-03-01", "Present"], "work": "Quantum Secure", "description": "\u2022 Optimized and managed Salesforce.com instance to create a useful and productive lead and opportunity management tool\n\u2022 Designed and executed various demand generation campaigns including webinars, tradeshows, roundtable dinners, online, direct mail and email\n\u2022 Implemented advanced marketing program analytics to track metrics, including campaign effectiveness, prospect engagement, funnel advancement, conversion rate and ROI to identify successes opportunities for improvement\n\u2022 Developed custom nurture tracks for prospects and existing customers designed to educate and engage them with relevant content as they move through the funnel\n\u2022 Lead efforts to build overall marketing automation strategy and foundation, including campaign flow templates, nurture paths, lead scoring, lead stages and best practices for the team to adopt\n\u2022 Continuously monitored and analyzed audience selection, timing, messaging, testing, creative development, and analysis of all campaigns", "title": "Marketing Program Manager"}, {"skills": ["marketing", "campaigns", "sales", "social media", "outbound", "management", "budget", "lead generation", "marketing automation", "email marketing", "seo", "marketing campaigns", "logistics", "contract negotiations", "marketing initiatives", "email campaigns", "promotional", "marketing promotions", "communications", "sales tools"], "time": ["2013-01-01", "2014-02-28"], "work": "Gilson, Inc", "description": "\u2022 Conception, development and execution of demand and lead generation marketing campaigns including direct and email marketing, promotions, landing pages, SEO, and support materials that align with business initiatives\n\u2022 Manage all aspects of trade show events (attendees ranging from 150-30,000 per event) including structure logistics, contract negotiations, staffing, promotional giveaways, graphics, pre/post-show marketing, show objectives, etc., often managing multiple shows at the same time; consistently came in under budget\n\u2022 Monitor and analyze effectiveness of all communications activities and outbound programs, including A/B testing for email campaigns, web content and social media involvement\n\u2022 Implementation and management of cloud applications/tools to support sales & marketing initiatives, including marketing automation and demand gen tools (Marketo, Google Adwords), and sales quoting tools improvement\n\u2022 Writing, editing and designing of inbound and outbound marketing content including emails, web and landing pages, brochures, social media, etc. - part of multi-touch creative campaigns", "title": "Senior Marketing Specialist"}, {"skills": ["marketing", "sales", "social media", "budget", "campaigns", "media placement", "management", "advertising", "lead generation", "crm", "sales team", "roi", "digital advertising", "product positioning", "analysis", "marketing budget", "printers", "newsletters", "hygiene", "coordination"], "time": ["2011-05-01", "2013-01-01"], "work": "", "description": "\u2022 Actively maintain consistent product positioning and accurate information across all public mediums (websites, newsletters, social media, print publications, etc.)\n\u2022 Support of sales team of 30+ across the country at any stage of the sales process\n\u2022 Assistance with the maintenance of company-wide CRM, improving upon best practices and ensuring good data hygiene for best campaign performance\n\u2022 Improvement of monthly analysis of key marketing initiatives to assess the performance of marketing campaigns in order to gain insight on ROI\n\u2022 Management of media/advertising budget of over $500K and Marketing budget exceeding $1M; dictating all media placement/design and leading company transition into digital advertising\n\u2022 Integral part of lead generation improvement of over 900% through improved media placement and social media\n\u2022 Coordination of marketing efforts with external suppliers (graphic/marketing agencies, printers, mail-houses, etc.)", "title": "Marketing Specialist"}, {"skills": ["classroom", "negotiation", "communication", "community", "courses", "flexibility", "thai", "events", "independence"], "time": ["2010-05-01", "2011-03-01"], "work": "Supaluck School", "description": "\u2022 Set up classroom meetings and events to help parents become more involved and build rapport within community\n\u2022 Learned conversational Thai and honed in on my verbal and non-verbal communication skills\n\u2022 Lead courses focusing on Reading Comprehension, Listening Skills, Writing and Speaking\n\u2022 Increased flexibility, independence, and negotiation skills", "title": "Intensive ESL Teacher"}, {"skills": ["marketing", "sales", "advertising", "social media", "management", "budget", "crm", "sales team", "direct marketing", "media plan", "facebook", "database", "collateral", "networking", "sales meetings", "research", "green", "clients", "features", "house"], "time": ["2008-05-01", "2010-04-30"], "work": "T. Wall Properties", "description": "\u2022 Supported Sales & Marketing team through creation of sales collateral, advertising, direct marketing and lease proposal booklets\n\u2022 Completed a strong, visible social media plan using Twitter, LinkedIn, Facebook, CEO blog, etc.\n\u2022 Managed complex prospect database/CRM system and implemented new procedures making it a more valuable research tool company wide\n\u2022 Composed new layout for company website to include a green link in order to educate potential clients of the company's green features; tracked web page traffic; responsible for website updates\n\u2022 Planned, budgeted, and hosted large corporate events including annual investor meetings (over 250 people), broker networking functions, and ground breaking/open house events\n\u2022 Acquired, analyzed and interpreted consumer and market information to optimize value for brokers\n\u2022 Assisted in creation and management of department budget of over $120,000 positioning advertising/marketing spending\n\u2022 Collaborated closely with Sales team; led weekly sales meetings to evaluate quarterly and individual goals\n\u2022 Contributed to the response to and research for RFP's & RFQ's", "title": "Marketing Intern/Assistant and Sales and Leasing Coordinator"}]}]


class SeniorityFinder:

    def __init__(self):
        clf = load(MODEL_PATH)
        self.classifier = clf

    def get_seniority(self,profiles):

        feature_vectors = [self.get_feature_vector(profile) for profile in profiles]
        preds = self.classifier.predict(feature_vectors)
        return preds

    def get_feature_vector(self, profile):
        processed_profile = []

        educations = profile.get('education')
        experiences = profile.get('experience')

        # Number of educations
        processed_profile.append(len(educations))

        # Experience count
        processed_profile.append(len(experiences))

        # Work tenure info
        longest_tenure, total_work_ex = get_longest_tenure(experiences)
        processed_profile += [longest_tenure, total_work_ex]

        # Using proxy for degrees he has mentioned
        processed_profile += get_proxy_for_degree(educations)

        # Days since last education
        processed_profile += [time_since_last_education(educations)]

        return processed_profile


if __name__ == "__main__":

    # Trying out seniority finder
    sf = SeniorityFinder()
    print(sf.get_seniority(SAMPLE_PROFILES))



