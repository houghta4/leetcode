import random
import httpx
import asyncio

# Constants
LEETCODE_API_ENDPOINT = 'https://leetcode.com/graphql'
DAILY_CODING_CHALLENGE_QUERY = '''
    query {
        activeDailyCodingChallengeQuestion {
            date
            userStatus
            link
            question {
                questionId
                title
                titleSlug
                difficulty
            }
        }
    }
'''
USER_SUBMISSIONS_QUERY = '''
    query recentAcSubmissions($username: String!) {
        recentAcSubmissionList(username: $username) {
            id
            title
            titleSlug
            timestamp
        }
    }
'''

ALL_PROBLEMS_QUERY = '''
    query ($difficulty: DifficultyEnum!) {
        questionList(filters: {difficulty: $difficulty}) {
            data {
                questionId
                title
                titleSlug
                difficulty
            }
        }
    }
'''

PROBLEM_QUERY = '''
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            total: totalNum
            questions: data {
                acRate
                difficulty
                freqBar
                frontendQuestionId: questionFrontendId
                isFavor
                paidOnly: isPaidOnly
                status
                title
                titleSlug
                topicTags {
                    name
                    id
                    slug
                }
                hasSolution
                hasVideoSolution
            }
        }
    }
'''

async def fetch_leetcode_data(query, variables=None):
    '''send req to leetcode api'''
    headers = {'Content-Type': 'application/json'}
    payload = {'query': query, 'variables': variables or {}}

    async with httpx.AsyncClient() as client:
        response = await client.post(LEETCODE_API_ENDPOINT, json=payload, headers=headers)
        return response.json()

async def fetch_daily_problem(message_only=False):
    '''get daily problem from leetcode'''
    daily_challenge = await fetch_leetcode_data(DAILY_CODING_CHALLENGE_QUERY)
    problem_data = daily_challenge.get('data', {}).get('activeDailyCodingChallengeQuestion', {}).get('question', {})

    if not problem_data:
        return 'Error getting problem_data'
    
    problem_title = problem_data.get('title', 'Error getting problem_title')
    problem_slug = problem_data.get('titleSlug', 'Error getting problem_slug')
    problem_difficulty = problem_data.get('difficulty', 'Error getting problem_difficulty')
    link = f'https://leetcode.com/problems/{problem_slug}'

    display_message = f'\n🔹 **Daily Coding Challenge** 🔹\n' \
           f'📌 **Title:** {problem_title}\n' \
           f'📄 **Difficulty:** {problem_difficulty}\n' \
           f'🔗 **Link:** {link}'
    
    if message_only:
        return display_message
    
    return {
        'title': problem_title,
        'slug': problem_slug,
        'difficulty': problem_difficulty,
        'link': link,
        'message': display_message
    }

async def check_user_completion(username, problem_slug):
    '''check if user has completed `problem_slug`'''
    user_data = await fetch_leetcode_data(USER_SUBMISSIONS_QUERY, {'username': username})
    
    if not user_data:
        return 'Error getting user_data'
    
    recent_submissions = user_data.get('data', {}).get('recentAcSubmissionList', [])

    if not recent_submissions:
        return f'⚠️ **_{username}_ has no submissions. Double check your spelling **'

    solved_today = any(sub.get('titleSlug') == problem_slug for sub in recent_submissions)

    if solved_today:
        return f'✅ **_{username}_ has completed today\'s challenge!** 🎉'
    else:
        return f'❌ **_{username}_ has not completed today\'s challenge yet.** 👎'

async def check_daily_completion(username):
    '''check if user has compelted the daily problem'''
    # get daily problem
    daily_problem = await fetch_daily_problem()
    if not daily_problem: 
        return

    user_completion = await check_user_completion(username, daily_problem['slug'])
    return f'{daily_problem["message"]}\n\n{user_completion}'


async def fetch_problem(problem_id):
    '''get a specific problem from leetcode'''
    pass

async def fetch_problem_by_difficulty(difficulty):
    '''get a random problem given a difficulty'''
    total = await fetch_total_difficulty_questions(difficulty)
    skip = random.randint(0, total - 1)
    print(f'total: {total}, skip: {skip}')

    variables = {"categorySlug": "", "limit": 500, "skip": skip, "filters": {'difficulty': difficulty}}
    all_problems = await fetch_leetcode_data(PROBLEM_QUERY, variables)
    questions = all_problems.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])

    #TODO: break this into a helper since it shares with fetch_daily
    if not questions:
        return 'Error getting question'
    problem_data = [q for q in questions if not q['paidOnly']][0]
    problem_title = problem_data.get('title', 'Error getting problem_title')
    problem_slug = problem_data.get('titleSlug', 'Error getting problem_slug')
    problem_difficulty = problem_data.get('difficulty', 'Error getting problem_difficulty')
    link = f'https://leetcode.com/problems/{problem_slug}'

    display_message = f'\n🔹 **Daily Coding Challenge** 🔹\n' \
           f'📌 **Title:** {problem_title}\n' \
           f'📄 **Difficulty:** {problem_difficulty}\n' \
           f'🔗 **Link:** {link}'

    #TODO: not sure if all we want is display or to check if we have done it
    return display_message

async def fetch_total_difficulty_questions(difficulty):
    variables = {"categorySlug": "", "limit": 1, "skip": 0, "filters": {'difficulty': difficulty}}
    all_problems = await fetch_leetcode_data(PROBLEM_QUERY, variables)
    total = all_problems.get('data', {}).get('problemsetQuestionList', {}).get('total', -1)
    return total

#testing
if __name__ == '__main__':
    username = 'contain15percentjuice'
    # daily = asyncio.run(fetch_daily_problem())
    # print(daily['message'])
    # completed = asyncio.run(check_daily_completion('asdfasdfasdfasdfasdfasdfasdfffdzxcv'))
    # print(completed)
    # completed2 = asyncio.run(check_daily_completion(username))
    # print(completed2)
    asyncio.run(fetch_problem_by_difficulty('EASY'))
    # asyncio.run(check_daily_completion('choughtaling5'))
