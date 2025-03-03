from db import Database

DISCORD_ID = int(108735803651325952)

db = Database()

db.add_user(DISCORD_ID)
db.add_user(int(262789642590355477))
before_notify_status = db.get_notify(DISCORD_ID)
print(f"Notify Status: {before_notify_status}")
db.set_notify(DISCORD_ID, True)
after_notify_status = db.get_notify(DISCORD_ID)
print(f"Notify set to True: {after_notify_status}")

before_score = db.get_score(DISCORD_ID)
print(f"Score: {before_score}")
db.update_score(DISCORD_ID, 10)
after_score = db.get_score(DISCORD_ID)
print(f"After 10 added to score: {after_score}")

before_username = db.get_leetcode_username(DISCORD_ID)
print(f'Leetcode username: {before_username}')
db.set_leetcode_username(DISCORD_ID, "contain15percentjuice")
after_username = db.get_leetcode_username(DISCORD_ID)
print(f'Leetcode username: {after_username}')

before_username = db.get_discord_username(DISCORD_ID)
print(f'discord username: {before_username}')
db.set_discord_username(DISCORD_ID, "Vince")
after_username = db.get_discord_username(DISCORD_ID)
print(f'discord username: {after_username}')


db.update_user(DISCORD_ID, notify=False)
users = db.get_all_users()

for user in users:
    _, discord_id, discord_username, leetcode_username, notify, score = user
    print(f'{discord_id} | {discord_username} | {leetcode_username} | Notify: {notify} | Score: {score}')
db.commit()
db.close()
