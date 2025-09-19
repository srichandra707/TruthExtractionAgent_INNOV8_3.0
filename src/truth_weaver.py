import json
import re
import logging
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import difflib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TruthWeaver:
    def __init__(self):
        """Initialize the Truth Weaver system"""
        logger.info("🔮 Initializing Truth Weaver - Whispering Shadows Analyzer")
        
        # Technical skills patterns
        self.programming_languages = {
            'python': ['python', ' py ', 'django', 'flask', 'pandas', 'numpy'],
            'javascript': ['javascript', ' js', 'node', 'react', 'angular', 'vue'],
            'java': ['java', 'spring', 'hibernate'],
            'c++': ['c++', 'cpp', 'c plus plus'],
            'go': ['golang', ' go '],
            'rust': ['rust'],
            'sql': ['sql', 'database', 'mysql', 'postgresql'],
            'c' : ['c programming', ' c '],
            'ruby': ['ruby', 'rails']
        }
        
        # Experience indicators
        self.experience_patterns = {
            'years': r'(\d+)\s*(?:years?|yrs?)',
            'months': r'(\d+)\s*(?:months?|mos?)',
            'beginner': ['beginner', 'starting', 'new to', 'learning', 'just started'],
            'intermediate': ['intermediate', 'some experience', 'working knowledge'],
            'advanced': ['advanced', 'expert', 'master', 'senior', 'lead', 'architect']
        }
        
        # Leadership and team patterns
        self.leadership_patterns = {
            'team_size': r'(?:team|group)\s+of\s+(\d+)|(\d+)\s+(?:people|members|developers)',
            'leadership_roles': ['lead', 'manager', 'supervisor', 'director', 'head of', 'senior'],
            'individual': ['alone', 'solo', 'individual', 'myself', 'on my own']
        }
        
    def read_input_file(self, filename: str = 'input.txt') -> str:
        """Read the converted audio transcript"""
        logger.info(f"📖 Reading input file: {filename}")
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.info(f"✅ Successfully read {len(content)} characters from input file")
                return content
        except FileNotFoundError:
            logger.error(f"❌ Input file {filename} not found")
            raise
        except Exception as e:
            logger.error(f"❌ Error reading input file: {e}")
            raise
    
    def parse_sessions(self, content: str) -> Dict[str, List[str]]:
        """Parse the content into sessions for each shadow agent"""
        logger.info("🔍 Parsing sessions from transcript content")
        
        sessions_data = defaultdict(list)
        
        # Try to identify session patterns
        session_patterns = [
            r'Session\s+(\d+)[:\s]*(.+?)(?=Session\s+\d+|$)',
            r'subject[:\s]*(\w+).*?session[:\s]*(\d+)[:\s]*(.+?)(?=session|subject|$)',
            r'(\w+).*?session[:\s]*(\d+)[:\s]*(.+?)(?=session|subject|$)'
        ]
        
        # Split content by likely session boundaries
        lines = content.split('\n')
        current_subject = "unknown_shadow"
        current_session = 1
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for subject/shadow identifiers
            subject_match = re.search(r'(?:subject|shadow|agent)[:\s]*([a-zA-Z0-9_]+)', line, re.IGNORECASE)
            if subject_match:
                # Save previous session if exists
                if current_content:
                    sessions_data[current_subject].append(' '.join(current_content))
                    current_content = []
                current_subject = subject_match.group(1).lower()
                logger.info(f"👤 Identified subject: {current_subject}")
                continue
            
            # Check for session identifiers
            session_match = re.search(r'session[:\s]*(\d+)', line, re.IGNORECASE)
            if session_match:
                # Save previous session if exists
                if current_content:
                    sessions_data[current_subject].append(' '.join(current_content))
                    current_content = []
                current_session = int(session_match.group(1))
                logger.info(f"📝 Processing Session {current_session} for {current_subject}")
                continue
            
            # Add line to current session content
            current_content.append(line)
        
        # Don't forget the last session
        if current_content:
            sessions_data[current_subject].append(' '.join(current_content))
        
        # If no clear session structure, treat as single subject with multiple sessions
        if not sessions_data and content.strip():
            # Split content roughly into 5 parts (assuming 5 sessions)
            content_parts = content.split('\n\n') if '\n\n' in content else [content]
            for i, part in enumerate(content_parts[:5]):
                if part.strip():
                    sessions_data["shadow_agent"].append(part.strip())
        
        logger.info(f"✅ Parsed {len(sessions_data)} subjects with sessions")
        for subject, sessions in sessions_data.items():
            logger.info(f"  - {subject}: {len(sessions)} sessions")
        
        return dict(sessions_data)
    
    def extract_programming_experience(self, sessions: List[str]) -> Tuple[str, str]:
        """Extract programming experience and language from sessions"""
        logger.info("⚡ Extracting programming experience and language")
        
        all_text = ' '.join(sessions).lower()
        
        # Extract years/months of experience
        years_matches = re.findall(self.experience_patterns['years'], all_text)
        months_matches = re.findall(self.experience_patterns['months'], all_text)
        
        experience_claims = []
        if years_matches:
            for year in years_matches:
                try:
                    experience_claims.append(int(year) * 12)  # Convert to months
                    logger.info(f"  📊 Found experience claim: {year} years")
                except ValueError:
                    continue
        
        if months_matches:
            for month in months_matches:
                try:
                    experience_claims.append(int(month))
                    logger.info(f"  📊 Found experience claim: {month} months")
                except ValueError:
                    continue
        
        # Determine most likely experience level
        if experience_claims:
            # Take median to avoid outliers from lies
            experience_months = sorted(experience_claims)[len(experience_claims)//2]
            if experience_months < 12:
                experience = f"{experience_months} months"
            else:
                experience = f"{experience_months // 12}-{(experience_months // 12) + 1} years"
        else:
            # Look for qualitative indicators
            if any(word in all_text for word in self.experience_patterns['beginner']):
                experience = "beginner"
            elif any(word in all_text for word in self.experience_patterns['advanced']):
                experience = "advanced"
            else:
                experience = "unknown"
        
        # Extract programming language
        detected_language = "unknown"
        for lang, keywords in self.programming_languages.items():
            if any(keyword in all_text for keyword in keywords):
                detected_language = lang
                logger.info(f"  💻 Detected programming language: {lang}")
                break
        
        logger.info(f"✅ Programming experience extracted: {experience}, Language: {detected_language}")
        return experience, detected_language
    
    def extract_skill_mastery(self, sessions: List[str], experience: str) -> str:
        """Determine skill mastery level based on sessions and experience"""
        logger.info("🎯 Determining skill mastery level")
        
        all_text = ' '.join(sessions).lower()
        
        # Check for explicit mastery claims
        if any(word in all_text for word in self.experience_patterns['advanced']):
            mastery = "advanced"
        elif any(word in all_text for word in self.experience_patterns['beginner']):
            mastery = "beginner"
        elif any(word in all_text for word in self.experience_patterns['intermediate']):
            mastery = "intermediate"
        else:
            # Infer from experience
            if "months" in experience and not any(char.isdigit() and int(char) > 12 for char in experience.split()):
                mastery = "beginner"
            elif "year" in experience:
                years = re.findall(r'\d+', experience)
                if years and int(years[0]) >= 5:
                    mastery = "advanced"
                else:
                    mastery = "intermediate"
            else:
                mastery = "intermediate"
        
        logger.info(f"✅ Skill mastery determined: {mastery}")
        return mastery
    
    def extract_leadership_and_team_info(self, sessions: List[str]) -> Tuple[str, str]:
        """Extract leadership claims and team experience"""
        logger.info("👥 Extracting leadership and team information")
        
        all_text = ' '.join(sessions).lower()
        
        # Check for leadership roles
        has_leadership = any(role in all_text for role in self.leadership_patterns['leadership_roles'])
        
        # Check for team size mentions
        team_size_matches = re.findall(self.leadership_patterns['team_size'], all_text)
        team_sizes = []
        for match in team_size_matches:
            for group in match:
                if group:
                    try:
                        team_sizes.append(int(group))
                    except ValueError:
                        continue
        
        # Check for individual work indicators
        works_alone = any(indicator in all_text for indicator in self.leadership_patterns['individual'])
        
        # Determine leadership claims
        if has_leadership or team_sizes:
            leadership_claims = "claimed leadership experience"
            logger.info("  👨‍💼 Found leadership claims")
        else:
            leadership_claims = "no leadership claims"
            logger.info("  👤 No leadership claims found")
        
        # Determine team experience
        if works_alone:
            team_experience = "individual contributor"
            logger.info("  🏃‍♂️ Individual contributor pattern detected")
        elif team_sizes:
            max_team_size = max(team_sizes)
            team_experience = f"team member/lead ({max_team_size} person team)"
            logger.info(f"  👥 Team size mentioned: {max_team_size}")
        else:
            team_experience = "unknown team experience"
        
        logger.info(f"✅ Leadership and team info extracted")
        return leadership_claims, team_experience
    
    def extract_skills_and_keywords(self, sessions: List[str]) -> List[str]:
        """Extract technical skills and relevant keywords"""
        logger.info("🔧 Extracting technical skills and keywords")
        
        all_text = ' '.join(sessions).lower()
        
        # Common technical keywords
        tech_keywords = [
            ' machine learning ', ' ml ', ' ai ', 'artificial intelligence',
            'data science', 'analytics', 'big data',
            'web development', 'frontend', 'backend', 'full stack',
            'database', 'sql', 'nosql', 'mongodb', 'postgresql',
            'cloud', ' aws ', 'azure', 'gcp', 'docker', 'kubernetes',
            ' api ', ' rest ', 'graphql', 'microservices',
            'testing', 'unit testing', 'integration testing',
            'agile', 'scrum', 'devops', 'ci/cd'
        ]
        
        found_skills = []
        for keyword in tech_keywords:
            if keyword in all_text:
                found_skills.append(keyword.title())
                logger.info(f"  🎯 Found skill: {keyword}")
        
        # Also check for programming language specific skills
        for lang, lang_keywords in self.programming_languages.items():
            for keyword in lang_keywords:
                if keyword in all_text and keyword not in found_skills:
                    found_skills.append(keyword.title())
        
        logger.info(f"✅ Extracted {len(found_skills)} technical skills")
        return found_skills
    
    def detect_deception_patterns(self, sessions: List[str]) -> List[Dict[str, Any]]:
        """Detect contradiction patterns across sessions"""
        logger.info("🕵️ Analyzing deception patterns and contradictions")
        
        deception_patterns = []
        
        # Extract all experience claims across sessions
        experience_claims = []
        for i, session in enumerate(sessions):
            session_lower = session.lower()
            
            # Look for years
            years_in_session = re.findall(self.experience_patterns['years'], session_lower)
            for year in years_in_session:
                try:
                    experience_claims.append((i+1, f"{year} years"))
                    logger.info(f"  📝 Session {i+1}: Found experience claim '{year} years'")
                except ValueError:
                    continue
            
            # Look for months
            months_in_session = re.findall(self.experience_patterns['months'], session_lower)
            for month in months_in_session:
                try:
                    experience_claims.append((i+1, f"{month} months"))
                    logger.info(f"  📝 Session {i+1}: Found experience claim '{month} months'")
                except ValueError:
                    continue
        
        # Check for contradictions in experience claims
        if len(set([claim[1] for claim in experience_claims])) > 1:
            unique_claims = list(set([claim[1] for claim in experience_claims]))
            deception_patterns.append({
                "lie_type": "experience_inflation",
                "contradictory_claims": unique_claims,
                "sessions_involved": [claim[0] for claim in experience_claims]
            })
            logger.info(f"  ⚠️  Found experience contradictions: {unique_claims}")
        
        # Check for leadership contradictions
        leadership_sessions = []
        individual_sessions = []
        
        for i, session in enumerate(sessions):
            session_lower = session.lower()
            
            if any(role in session_lower for role in self.leadership_patterns['leadership_roles']):
                leadership_sessions.append(i+1)
            
            if any(indicator in session_lower for indicator in self.leadership_patterns['individual']):
                individual_sessions.append(i+1)
        
        if leadership_sessions and individual_sessions:
            deception_patterns.append({
                "lie_type": "leadership_contradiction",
                "contradictory_claims": ["claimed leadership", "works alone"],
                "sessions_involved": leadership_sessions + individual_sessions
            })
            logger.info(f"  ⚠️  Found leadership contradictions between sessions")
        
        # Check for confidence level changes (emotional patterns)
        confidence_levels = []
        for i, session in enumerate(sessions):
            session_lower = session.lower()
            
            if any(word in session_lower for word in ['confident', 'sure', 'definitely', 'absolutely']):
                confidence_levels.append((i+1, 'confident'))
            elif any(word in session_lower for word in ['maybe', 'perhaps', 'not sure', 'uncertain']):
                confidence_levels.append((i+1, 'uncertain'))
            elif any(word in session_lower for word in ['sobbing', 'crying', 'breakdown', 'emotional']):
                confidence_levels.append((i+1, 'emotional_breakdown'))
        
        if len(set([level[1] for level in confidence_levels])) > 2:
            deception_patterns.append({
                "lie_type": "emotional_inconsistency",
                "contradictory_claims": [level[1] for level in confidence_levels],
                "sessions_involved": [level[0] for level in confidence_levels]
            })
            logger.info(f"  ⚠️  Found emotional inconsistencies across sessions")
        
        logger.info(f"✅ Detected {len(deception_patterns)} deception patterns")
        return deception_patterns
    
    def analyze_shadow(self, shadow_id: str, sessions: List[str]) -> Dict[str, Any]:
        """Analyze a single shadow agent's testimonies"""
        logger.info(f"🔮 Analyzing Shadow Agent: {shadow_id}")
        logger.info(f"  📊 Processing {len(sessions)} sessions")
        
        # Extract programming experience and language
        experience, language = self.extract_programming_experience(sessions)
        
        # Determine skill mastery
        skill_mastery = self.extract_skill_mastery(sessions, experience)
        
        # Extract leadership and team information
        leadership_claims, team_experience = self.extract_leadership_and_team_info(sessions)
        
        # Extract technical skills
        skills_keywords = self.extract_skills_and_keywords(sessions)
        
        # Detect deception patterns
        deception_patterns = self.detect_deception_patterns(sessions)
        
        # Compile analysis results
        analysis = {
            "shadow_id": shadow_id,
            "revealed_truth": {
                "programming_experience": experience,
                "programming_language": language,
                "skill_mastery": skill_mastery,
                "leadership_claims": leadership_claims,
                "team_experience": team_experience,
                "skills_and_other_keywords": skills_keywords
            },
            "deception_patterns": deception_patterns
        }
        
        logger.info(f"✅ Analysis complete for {shadow_id}")
        return analysis
    
    def process_transcript(self, filename: str = 'input.txt') -> List[Dict[str, Any]]:
        """Main processing function"""
        logger.info("🚀 Starting Truth Weaver analysis")
        
        # Read input file
        content = self.read_input_file(filename)
        
        # Parse sessions
        sessions_data = self.parse_sessions(content)
        
        # Analyze each shadow
        results = []
        for shadow_id, sessions in sessions_data.items():
            if sessions:  # Only process if there are sessions
                analysis = self.analyze_shadow(shadow_id, sessions)
                results.append(analysis)
        
        logger.info(f"🎉 Truth Weaver analysis complete! Processed {len(results)} shadow agents")
        return results
    
    def save_results(self, results: List[Dict[str, Any]], output_filename: str = 'output.txt'):
        """Save results to output file"""
        logger.info(f"💾 Saving results to {output_filename}")
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as file:
                # Write JSON format results
                for result in results:
                    file.write(json.dumps(result, indent=2, ensure_ascii=False))
                    file.write('\n' + '='*50 + '\n')
                
                logger.info(f"✅ Results saved successfully to {output_filename}")
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")
            raise
    
    def create_json_output(self, results: List[Dict[str, Any]], json_filename: str = 'truth_analysis.json'):
        """Create clean JSON output file"""
        logger.info(f"📄 Creating JSON output: {json_filename}")
        
        try:
            with open(json_filename, 'w', encoding='utf-8') as file:
                json.dump(results, file, indent=2, ensure_ascii=False)
                logger.info(f"✅ JSON output saved to {json_filename}")
        except Exception as e:
            logger.error(f"❌ Error creating JSON output: {e}")
            raise

def main():
    """Main execution function"""
    print("🔮 Truth Weaver - Whispering Shadows Analyzer")
    print("=" * 50)
    
    try:
        # Initialize Truth Weaver
        weaver = TruthWeaver()
        
        # Process the transcript
        results = weaver.process_transcript('input.txt')
        
        # Save results
        weaver.save_results(results, 'output.txt')
        weaver.create_json_output(results, 'truth_analysis.json')
        
        print("\n🎉 Analysis Complete!")
        print(f"📊 Analyzed {len(results)} shadow agents")
        print("📁 Files created:")
        print("  - output.txt (detailed results)")
        print("  - truth_analysis.json (JSON format)")
        
    except FileNotFoundError:
        print("❌ Error: input.txt file not found!")
        print("Please ensure the input.txt file exists in the same directory.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    main()