#ifndef VI_AI_H
#define VI_AI_H

#include "board.h"

#include <algorithm>
#include <unordered_map>
#include <utility>

namespace vi
{
	struct ai
	{
		using depth_type       = unsigned;
		using probability_type = double;

		action           find_move(board);
		board::heuristic score_move_node(board, depth_type, probability_type);
		board::heuristic score_tilespawn_node(board, depth_type, probability_type);

		struct transposition_table_entry
		{
			depth_type       depth;
			board::heuristic score;
		};

		std::unordered_map<board::state, transposition_table_entry> transposition_table{};

		unsigned max_depth = 0;
		unsigned moves_evaluated = 0;
		unsigned cache_hits = 0;
		unsigned cache_misses = 0;
		unsigned probability_prune_hits = 0;
		unsigned probability_prune_misses = 0;
	};
}

#endif // VI_AI_H
