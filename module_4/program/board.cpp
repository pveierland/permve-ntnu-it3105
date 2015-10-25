#include "board.h"

#include <cstdio>

namespace vi
{
    std::vector<board::heuristic> board::heuristic_lut = board::build_heuristic_lut();
    board::move_luts              board::move_lut      = board::build_move_lut();
    std::vector<board::score>     board::score_lut     = board::build_score_lut();

    std::ostream&
    operator<<(std::ostream& os, const board& board)
    {
        for (unsigned row = 0; row != 4; ++row)
        {
            for (unsigned column = 0; column != 4; ++column)
            {
                printf("%5d ", board.get_value(row, column));
            }
            std::cout << std::endl;
        }
    }

    std::vector<board::heuristic>
    board::build_heuristic_lut()
    {
        std::vector<board::heuristic> heuristic_lut(board::lut_size);

        const float SCORE_LOST_PENALTY        = 200000.0;
        const float SCORE_MONOTONICITY_POWER  = 4.0;
        const float SCORE_MONOTONICITY_WEIGHT = 47.0;
        const float SCORE_SUM_POWER           = 3.5;
        const float SCORE_SUM_WEIGHT          = 11.0;
        const float SCORE_MERGES_WEIGHT       = 700.0;
        const float SCORE_EMPTY_WEIGHT        = 270.0;

        for (int row = 0; row != 65536; ++row)
        {
            const int num_empty =
                static_cast<int>(((row >>  0) & 0xF) == 0) +
                static_cast<int>(((row >>  4) & 0xF) == 0) +
                static_cast<int>(((row >>  8) & 0xF) == 0) +
                static_cast<int>(((row >> 12) & 0xF) == 0);

            heuristic_lut[row] =
                SCORE_LOST_PENALTY + SCORE_EMPTY_WEIGHT * num_empty;
        }

        return heuristic_lut;
    }

    board::move_luts
    board::build_move_lut()
    {
        board::move_luts move_lut{};

        move_lut.up    = std::vector<board::state>(board::lut_size);
        move_lut.down  = std::vector<board::state>(board::lut_size);
        move_lut.left  = std::vector<board::row>(board::lut_size);
        move_lut.right = std::vector<board::row>(board::lut_size);

        for (unsigned row = 0; row != board::lut_size; ++row)
        {
            board::row result        = 0;
            auto       output_offset = 0U;

            auto index = 0U;
            while (index < 3U)
            {
                const auto offset       = 4U * index;
                const auto current_cell = (row & (0xFU << offset)) >> offset;

                if (current_cell)
                {
                    const auto next_cell = (row & (0xFU << (offset + 4U))) >> (offset + 4);

                    if (current_cell == next_cell)
                    {
                        result |= (current_cell + 1U) << output_offset;
                        ++index;
                    }
                    else
                    {
                        result |= current_cell << output_offset;
                    }

                    output_offset += 4U;
                }

                ++index;
            }

            if (index < 4U)
            {
                const auto offset = 4U * index;
                result |= ((row & (0xFU << offset)) >> offset) << output_offset;
            }

            const auto rev_result   = reverse_row(result);
            const auto rev_row      = reverse_row(row);

            move_lut.up[row]        = unpack_column(row)     ^ unpack_column(result);
            move_lut.down[rev_row]  = unpack_column(rev_row) ^ unpack_column(rev_result);
            move_lut.left[row]      = row     ^ result;
            move_lut.right[rev_row] = rev_row ^ rev_result;
        }

        return move_lut;
    }

    std::vector<board::score>
    board::build_score_lut()
    {
        std::vector<board::score> score_lut(board::lut_size);

        for (auto row = 0U; row != board::lut_size; ++row)
        {
            board::score score{};

            for (auto i = 0U; i != 4; ++i)
            {
                const auto rank = (row >> (4U * i)) & 0xFU;
                if (rank >= 2)
                {
                    score += (rank - 1) * (1 << rank);
                }
            }

            score_lut[row] = score;
        }

        return score_lut;
    }
}

