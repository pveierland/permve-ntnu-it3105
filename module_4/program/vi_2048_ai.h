#ifndef VI_2048_AI_H
#define VI_2048_AI_H

#include "vi_2048_board.h"

#include <algorithm>
#include <unordered_map>
#include <utility>

namespace vi
{
    struct ai
    {
        using depth_type       = unsigned;
        using probability_type = double;

        move_type        find_move(board);
        board::heuristic score_player_node(board, depth_type, probability_type);
        board::heuristic score_chance_node(board, depth_type, probability_type);

        struct transposition_table_entry
        {
            depth_type       depth;
            board::heuristic score;
        };

        std::unordered_map<board, transposition_table_entry> transposition_table{};

        unsigned depth_limit = 0;
        float    probability_limit = 0.0f; 

        unsigned max_depth = 0;
        unsigned moves_evaluated = 0;
        unsigned cache_hits = 0;
        unsigned cache_misses = 0;
        unsigned probability_prune_hits = 0;
        unsigned probability_prune_misses = 0;
    };
}

#endif // VI_2048_AI_H

