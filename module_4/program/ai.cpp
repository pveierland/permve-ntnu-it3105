#include "ai.h"

#include <iostream>

namespace vi
{
	action
	ai::find_move(const board board)
	{
		action best_move{};
		board::heuristic best_score{};

		for (int a = 0; a < 4; ++a)
		{
			const auto move = static_cast<action>(a);
			const auto new_board = board.move(move);

			if (new_board != board)
			{
				const auto score = score_tilespawn_node(board.move(move), 0, 1.0) + 0.000001;
				if (score > best_score)
				{
					best_score = score;
					best_move = move;
				}
			}
		}

		return best_move;
	}

	board::heuristic
	ai::score_move_node(const board board, const depth_type depth, const probability_type probability)
	{
		board::heuristic score{};

		for (unsigned move = 0; move != 4; ++move)
		{
			const auto new_board = board.move(static_cast<action>(move));
			++moves_evaluated;
			if (new_board != board)
			{
				score = std::max(score, score_tilespawn_node(new_board, depth + 1, probability));
			}
		}

		return score;
	}

	board::heuristic
	ai::score_tilespawn_node(const vi::board board, const depth_type depth, probability_type probability)
	{
		if (probability < 0.0001)
		{
			++probability_prune_hits;
			max_depth = std::max(max_depth, depth);
			return board.get_heuristic();
		}
		else
		{
			++probability_prune_misses;
		}

		if (depth >= 4)
		{
			max_depth = std::max(max_depth, depth);
			return board.get_heuristic();
		}

		auto entry = transposition_table.find(board.board_state);

		if (entry != transposition_table.end() && entry->second.depth <= depth)
		{
			++cache_hits;
			return entry->second.score;
		}
		else
		{
			++cache_misses;
		}

		const auto available = board.get_available_count();
		probability /= available;

		board::state board_state = board.board_state;
		board::state tmp = board_state;
		board::state tile = 1;

		board::heuristic score = {};

		while (tile)
		{
			if ((tmp & 0xF) == 0)
			{
				score += score_move_node(vi::board{ board_state | tile }, depth, probability * 0.9) * 0.9;
				score += score_move_node(vi::board{ board_state | (tile << 1) }, depth, probability * 0.1) * 0.1;
			}
			tmp >>= 4;
			tile <<= 4;
		}

		score /= available;

		transposition_table[board_state] = transposition_table_entry{ depth, score };

		return score;
	}
}
