import math

import trueskill


class Util:

    @staticmethod
    def get_probability(p1_skill, p2_skill):
        delta_mu = p1_skill.mu - p2_skill.mu
        sum_sigma = p1_skill.sigma ** 2 + p2_skill.sigma ** 2
        denom = math.sqrt(2 * (trueskill.BETA * trueskill.BETA) + sum_sigma)
        return trueskill.global_env().cdf(delta_mu / denom)