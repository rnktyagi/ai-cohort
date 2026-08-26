QUERY 1

SELECT plan_name, annual_deductible
FROM plans
WHERE plan_name = 'Gold PPO';

OUTPUT 1
  plan_name  annual_deductible
0  Gold PPO               2000

QUERY 2

SELECT COUNT(*) AS pending_claims
FROM claims
WHERE member_id = 'M1001'
AND status = 'Pending';

OUTPUT 2
   pending_claims
0               1

QUERY 3

SELECT plan_name, monthly_premium
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium ASC;

OUTPUT 3
    plan_name  monthly_premium
0  Bronze HMO              150
1  Silver HMO              300

QUERY 4

SELECT
    c.claim_id,
    c.member_id,
    c.procedure,
    c.claim_amount,
    c.status,
    p.plan_name,
    p.monthly_premium,
    p.annual_deductible
FROM claims c
JOIN plans p
ON c.plan_id = p.plan_id;

OUTPUT 4
  claim_id member_id procedure  claim_amount    status   plan_name  monthly_premium  annual_deductible
0    C1001     M1001     X-ray           250   Pending    Gold PPO              500               2000
1    C1002     M1001   Surgery          1200  Approved    Gold PPO              500               2000
2    C1003     M1002     X-ray           150    Denied  Silver HMO              300               1500
3    C1004     M1002   Surgery           900  Approved  Silver HMO              300               1500
4    C1005     M1003     X-ray            50   Pending  Bronze HMO              150               1000

QUERY 5

SELECT
    procedure,
    COUNT(*) AS claim_count
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC
LIMIT 5;

OUTPUT 5
  procedure  claim_count
0     X-ray            3
1   Surgery            2