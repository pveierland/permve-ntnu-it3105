#ifndef VI_AI_H
#define VI_AI_H

#include "board.h"

#include <unordered_map>
#include <utility>

namespace vi
{
    struct ai
    {
        using depth       = unsigned;
        using probability = double;

        action           find_move(board);
        board::heuristic score_move_node(board, depth, probability);
        board::heuristic score_tilespawn_node(board, depth, probability);

        struct transposition_table_entry
        {
            unsigned         depth;
            board::heuristic score;
        };

        std::unordered_map<board::state, transposition_table_entry> transposition_table{};

        unsigned max_depth       = 0;
        unsigned moves_evaluated = 0;
        unsigned cache_hits      = 0;
        unsigned leaf_nodes      = 0;
    };

    inline
    action
    ai::find_move(const board board)
    {
        struct
        {
            board::heuristic score;
            action           move;
        } best {};

        for (unsigned a = 0; a != 4; ++a)
        {
            const auto move      = static_cast<action>(a);
            const auto new_board = board.move(move);

//            if (new_board != board)
            {
                const auto score = score_tilespawn_node(board.move(move), 0, 1.0) + 0.000001;
                if (score > best.score)
                {
                    best.score = score;
                    best.move  = move;
                }
            }
        }

        return best.move;
    }

    inline
    board::heuristic
    ai::score_move_node(const board board, const depth depth, const probability probability)
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
    }

    inline
    board::heuristic
    ai::score_tilespawn_node(const vi::board board, const depth depth, probability probability)
    {
        //if (probability < 0.0001 or depth >= 2)
        if (depth >= 4)
        {
            ++leaf_nodes;
            max_depth = std::max(max_depth, depth);
            return board.get_heuristic();
        }

        //auto entry = transposition_table.find(board.board_state);

        //if (entry != transposition_table.end())
        //{
        //    if (entry->second.depth <= depth)
        //    {
        //        ++cache_hits;
        //        return entry->second.score;
        //    }
        //}

        const auto available = board.get_available_count();
        probability /= available;

        board::state board_state = board.board_state;
        board::state tile        = 1;

        board::heuristic score = {};

        while (tile)
        {
            if ((board_state & 0xF) == 0)
            {
                score += score_move_node(vi::board{board_state | tile}, depth, probability * 0.9) * 0.9;
                score += score_move_node(vi::board{board_state | (tile << 1)}, depth, probability * 0.1) * 0.1;
            }
            board_state >>= 4;
            tile        <<= 4;
        }

        score /= available;

        //transposition_table[board_state] = transposition_table_entry{depth, score};

        return score;
    }
}

#endif // VI_AI_H

