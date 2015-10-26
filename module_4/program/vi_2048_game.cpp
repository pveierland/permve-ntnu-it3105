#include "vi_2048_ai.h"
#include "vi_2048_board.h"
#include "vi_2048_game.h"

#include <iostream>
#include <random>

namespace vi
{
    std::default_random_engine rng{std::random_device{}()};
    auto tile_distribution = std::uniform_int_distribution<vi::board::state>{1, 10};
    auto move_count = 0;
    vi::ai ai{};

    vi::board current_board{};

    static inline
    vi::board
    insert_tile(vi::board board, vi::board::state tile, unsigned index)
    {
        vi::board::state board_state = board.board_state;

        for (;; --index)
        {
            while (board_state & 0xFU)
            {
                board_state >>= 4;
                tile        <<= 4;
            }

            if (!index)
            {
                break;
            }

            board_state >>= 4;
            tile        <<= 4;
        }

        return vi::board{board.board_state | tile};
    }

    static inline
    bool
    is_game_over()
    {
        vi::move_type move = vi::move::up;
        for (; move != vi::move::invalid; ++move)
        {
            if (current_board.move(move) != current_board)
            {
                break;
            }
        }
        return move == vi::move::invalid;
    }

    static inline
    vi::board::state
    random_tile()
    {
        return tile_distribution(rng) == 10 ? 2 : 1;
    }
    
    void
    configure(const unsigned depth_limit, const float probability_limit)
    {
        ai.depth_limit       = depth_limit;
        ai.probability_limit = probability_limit;
    }

    void
    reset_game()
    {
        current_board = insert_tile(
            vi::board{}, random_tile(), std::uniform_int_distribution<unsigned>{0, 15}(rng));
    }

    unsigned long
    step_game()
    {
        if (is_game_over())
        {
            printf("Game over! Highest tile: %u Final score: %.0f\n",
                   current_board.get_highest_value(),
                   current_board.get_score());
            return 0;
        }

        auto move = ai.find_move(current_board);

        printf("Current: %.2f Actual: %.0f Moves: %d Moves evaluated: %d Move %d. Cache %d hits / %d misses (%.2f%%). Pruned %d hits / %d misses (%.2f%%)\n",
            current_board.get_heuristic(),
            current_board.get_score(),
            move_count,
            ai.moves_evaluated,
            static_cast<int>(move),
            ai.cache_hits,
            ai.cache_misses,
            100.0 * ai.cache_hits / (ai.cache_hits + ai.cache_misses),
            ai.probability_prune_hits,
            ai.probability_prune_misses,
            100.0 * ai.probability_prune_hits / (ai.probability_prune_hits + ai.probability_prune_misses));

        ai.moves_evaluated = 0;
        ai.cache_hits = 0;
        ai.cache_misses = 0;
        ai.probability_prune_hits = 0;
        ai.probability_prune_misses = 0;
        ai.transposition_table.clear();

        current_board = current_board.move(move);

        ++move_count;

        auto num_available = current_board.get_available_count();
        if (num_available)
        {
            current_board = insert_tile(current_board,
                                random_tile(),
                                std::uniform_int_distribution<unsigned>{0, num_available - 1}(rng));
        }

        return current_board.board_state;
    }
}

