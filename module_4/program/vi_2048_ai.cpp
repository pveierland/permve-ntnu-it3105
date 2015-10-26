#include "vi_2048_ai.h"

namespace vi
{
    move_type
    ai::find_move(const board board)
    {
        move_type        best_move{};
        board::heuristic best_score{};

        for (vi::move_type move = vi::move::up;
             move != vi::move::invalid;
             ++move)
        {
            const auto new_board = board.move(move);

            if (new_board != board)
            {
                const auto score = score_chance_node(new_board, 0, 1.0f) + 0.000001;

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
    ai::score_player_node(const board            board,
                          const depth_type       depth,
                          const probability_type probability)
    {
        board::heuristic best_score{};

        for (vi::move_type move = vi::move::up;
             move != vi::move::invalid;
             ++move)
        {
            const auto new_board = board.move(move);

            ++moves_evaluated;

            if (new_board != board)
            {
                const auto score = score_chance_node(new_board, depth + 1, probability);
                best_score = std::max(best_score, score);
            }
        }

        return best_score;
    }

    board::heuristic
    ai::score_chance_node(const vi::board        board,
                          const depth_type       depth,
                          const probability_type probability)
    {
        if (probability < probability_limit)
        {
            ++probability_prune_hits;
            max_depth = std::max(max_depth, depth);

            return board.get_heuristic();
        }
        else
        {
            ++probability_prune_misses;
        }

        if (depth >= depth_limit)
        {
            max_depth = std::max(max_depth, depth);
            return board.get_heuristic();
        }

        const auto entry = transposition_table.find(board);

        if (entry != transposition_table.end() && entry->second.depth <= depth)
        {
            ++cache_hits;
            return entry->second.score;
        }
        else
        {
            ++cache_misses;
        }

        const auto available_tiles         = board.get_available_count();
        const auto successor_probability_2 = 0.9f * probability / available_tiles;
        const auto successor_probability_4 = 0.1f * probability / available_tiles;

        const board::state board_state = board.board_state;

        board::state tmp = board_state;
        board::state tile = 1;

        board::heuristic score = {};

        while (tile)
        {
            if ((tmp & 0xF) == 0)
            {
                score += score_player_node(vi::board{board_state | tile},
                                           depth,
                                           successor_probability_2) * 0.9f;

                score += score_player_node(vi::board{board_state | (tile << 1)},
                                           depth,
                                           successor_probability_4) * 0.1f;
            }

            tmp  >>= 4;
            tile <<= 4;
        }

        score /= available_tiles;

        transposition_table[board] = transposition_table_entry{depth, score};

        return score;
    }
}

