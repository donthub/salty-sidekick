import math

import trueskill


class Util:

    @staticmethod
    def get_probability(p1_skill, p2_skill):
        delta_mu = p1_skill.mu - p2_skill.mu
        sum_sigma = p1_skill.sigma ** 2 + p2_skill.sigma ** 2
        denom = math.sqrt(2 * (trueskill.BETA * trueskill.BETA) + sum_sigma)
        probability = trueskill.global_env().cdf(delta_mu / denom)
        return round(probability, 4)

    @staticmethod
    def get_probability_player_name(p1, p2):
        direct = p1.get_direct(p2.name)
        if direct.total > 0 and direct.wins != direct.losses:
            return p1.name if direct.wins > direct.losses else p2.name

        p1_skill = round(p1.skill.mu, 4)
        p2_skill = round(p2.skill.mu, 4)
        if p1_skill > p2_skill:
            return p1.name
        elif p2_skill > p1_skill:
            return p2.name
        return None

    @staticmethod
    def get_amount(amount):
        prefix = Util.get_prefix(amount)
        amount_from = str(abs(round(amount)))
        amount_to = ''

        index = 0
        for character in amount_from:
            amount_to += character
            if (len(amount_from) - index - 1) % 3 == 0 and index != len(amount_from) - 1:
                amount_to += ','
            index += 1

        return prefix + amount_to

    @staticmethod
    def get_prefix(amount):
        if amount > 0:
            return '+'
        elif amount < 0:
            return '-'
        else:
            return ''