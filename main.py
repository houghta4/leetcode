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

async def fetch_leetcode_data(query, variables=None):
    '''send req to leetcode api'''
    headers = {'Content-Type': 'application/json'}
    payload = {'query': query, 'variables': variables or {}}

    async with httpx.AsyncClient() as client:
        response = await client.post(LEETCODE_API_ENDPOINT, json=payload, headers=headers)
        return response.json()

async def check_daily_completion(username):
    '''check if user has compelted the daily problem'''
    # get daily problem
    daily_challenge = await fetch_leetcode_data(DAILY_CODING_CHALLENGE_QUERY)
    problem_data = daily_challenge.get('data', {}).get('activeDailyCodingChallengeQuestion', {}).get('question', {})

    if not problem_data:
        print('Error getting problem_data')
        return
    
    problem_title = problem_data.get('title', 'Error getting problem_title')
    problem_slug = problem_data.get('titleSlug', 'Error getting problem_slug')
    problem_difficulty = problem_data.get('difficulty', 'Error getting problem_difficulty')
    link = f'https://leetcode.com/problems/{problem_slug}'

    print('\n🔹 **Daily Coding Challenge** 🔹')
    print(f'📌 **Title:** {problem_title}')
    print(f'📄 **Difficulty:** {problem_difficulty}')
    print(f'🔗 **Link:** {link}')

    # get user's recently problems
    user_data = await fetch_leetcode_data(USER_SUBMISSIONS_QUERY, {'username': username})
    recent_submissions = user_data.get('data', {}).get('recentAcSubmissionList', [])

    solved_today = any(sub.get('titleSlug') == problem_slug for sub in recent_submissions)

    if solved_today:
        print(f'✅ **{username} has completed today\'s challenge!** 🎉')
    else:
        print(f'❌ **{username} has not completed today\'s challenge yet.** 👎')

async def check_problem_completion(username, problem_id):
    '''check if user has completed a specific problem by id'''
    pass

if __name__ == '__main__':
    username = 'contain15percentjuice'
    asyncio.run(check_daily_completion(username))
    asyncio.run(check_daily_completion('choughtaling5'))
