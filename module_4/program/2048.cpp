#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <limits>
#include <vector>

enum class action : unsigned
{
    up    = 0,
    down  = 1,
    left  = 2,
    right = 3
};

struct board
{
    using row       = std::uint16_t;
    using state     = std::uint64_t;
    using heuristic = float;
    using score     = float;

    static constexpr unsigned lut_size = std::numeric_limits<row>::max() + 1;

    struct move_luts
    {
        std::vector<state> up;
        std::vector<state> down;
        std::vector<row>   left;
        std::vector<row>   right;
    };

    static std::vector<heuristic> build_heuristic_lut();
    static move_luts              build_move_lut();
    static std::vector<score>     build_score_lut();

    board(const state board_state = 0)
        : board_state(board_state) { }

    board(const board&) = default;

    heuristic get_heuristic() const;
    score     get_score()     const;
    board     move(action)    const;

    unsigned
    get_raw_value(const unsigned row, const unsigned column) const
    {
        const auto offset = 16U * row + 4U * column;
        return (board_state >> offset) & 0xFU;
    }

    unsigned
    get_value(const unsigned row, const unsigned column) const
    {
        const auto raw = get_raw_value(row, column);
        return raw ? 1 << raw : 0;
    }

    void
    set_raw_value(const unsigned row, const unsigned column, const unsigned raw_value)
    {
        const auto offset = 16U * row + 4U * column;
        board_state = (board_state & ~(0x15U << offset)) | (raw_value << offset);
    }

    void
    set_value(const unsigned row, const unsigned column, const unsigned value)
    {
        const auto raw_value = value ? static_cast<unsigned>(std::log2(value)) : 0;
        set_raw_value(row, column, raw_value);
    }

    board
    spawn(const unsigned row, const unsigned column, const unsigned value) const
    {
        auto new_board = board{*this};
        new_board.set_value(row, column, value);
        return new_board;
    }

    static std::vector<heuristic> heuristic_lut;
    static std::vector<score>     score_lut;
    static move_luts              move_lut;

    state board_state;
};

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

inline
board::row
reverse_row(const board::row row)
{
    return ((row & 0xF000U) >> 12) | ((row & 0x0F00U) >> 4) |
           ((row & 0x000FU) << 12) | ((row & 0x00F0U) << 4);
}

board::state
transpose_board(const board::state board_state)
{
    const auto a1 = board_state & 0xF0F00F0FF0F00F0FULL;
    const auto a2 = board_state & 0x0000F0F00000F0F0ULL;
    const auto a3 = board_state & 0x0F0F00000F0F0000ULL;
    const auto a  = a1 | (a2 << 12) | (a3 >> 12);
    const auto b1 = a & 0xFF00FF0000FF00FFULL;
    const auto b2 = a & 0x00FF00FF00000000ULL;
    const auto b3 = a & 0x00000000FF00FF00ULL;
    return b1 | (b2 >> 24) | (b3 << 24);
}

inline
board::state
unpack_column(const board::row row)
{
    return 0x000F000F000F000FULL &
        ((static_cast<board::state>(row) <<  0) |
         (static_cast<board::state>(row) << 12) |
         (static_cast<board::state>(row) << 24) |
         (static_cast<board::state>(row) << 36));
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

inline
board::heuristic
board::get_heuristic() const
{
    const auto transposed_state = transpose_board(board_state);

    return (heuristic_lut[(board_state      >>  0) & 0xFFFF] +
            heuristic_lut[(board_state      >> 16) & 0xFFFF] +
            heuristic_lut[(board_state      >> 32) & 0xFFFF] +
            heuristic_lut[(board_state      >> 48) & 0xFFFF] +
            heuristic_lut[(transposed_state >>  0) & 0xFFFF] +
            heuristic_lut[(transposed_state >> 16) & 0xFFFF] +
            heuristic_lut[(transposed_state >> 32) & 0xFFFF] +
            heuristic_lut[(transposed_state >> 48) & 0xFFFF]);
}

inline
board::score
board::get_score() const
{
    return score_lut[(board_state >>  0) & 0xFFFFU] +
           score_lut[(board_state >> 16) & 0xFFFFU] +
           score_lut[(board_state >> 32) & 0xFFFFU] +
           score_lut[(board_state >> 48) & 0xFFFFU];
}

inline
board
board::move(const action action) const
{
    switch (action)
    {
        case ::action::up:
        {
            const auto transposed_state = transpose_board(board_state);
            return board{board_state ^
                (move_lut.up[(transposed_state >>  0) & 0xFFFF] <<  0) ^
                (move_lut.up[(transposed_state >> 16) & 0xFFFF] <<  4) ^
                (move_lut.up[(transposed_state >> 32) & 0xFFFF] <<  8) ^
                (move_lut.up[(transposed_state >> 48) & 0xFFFF] << 12)};
        }
        case ::action::down:
        {
            const auto transposed_state = transpose_board(board_state);
            return board{board_state ^
                (move_lut.down[(transposed_state >>  0) & 0xFFFF] <<  0) ^
                (move_lut.down[(transposed_state >> 16) & 0xFFFF] <<  4) ^
                (move_lut.down[(transposed_state >> 32) & 0xFFFF] <<  8) ^
                (move_lut.down[(transposed_state >> 48) & 0xFFFF] << 12)};
        }
        case ::action::left:
        {
            return board{board_state ^
                (static_cast<board::state>(move_lut.left[(board_state >>  0) & 0xFFFF]) <<  0) ^
                (static_cast<board::state>(move_lut.left[(board_state >> 16) & 0xFFFF]) << 16) ^
                (static_cast<board::state>(move_lut.left[(board_state >> 32) & 0xFFFF]) << 32) ^
                (static_cast<board::state>(move_lut.left[(board_state >> 48) & 0xFFFF]) << 48)};
        }
        case ::action::right:
        {
            return board{board_state ^
                (static_cast<board::state>(move_lut.right[(board_state >>  0) & 0xFFFF]) <<  0) ^
                (static_cast<board::state>(move_lut.right[(board_state >> 16) & 0xFFFF]) << 16) ^
                (static_cast<board::state>(move_lut.right[(board_state >> 32) & 0xFFFF]) << 32) ^
                (static_cast<board::state>(move_lut.right[(board_state >> 48) & 0xFFFF]) << 48)};
        }
        default:
        {
            assert(0);
        }
    }
}

std::vector<board::heuristic> board::heuristic_lut = board::build_heuristic_lut();
board::move_luts              board::move_lut      = board::build_move_lut();
std::vector<board::score>     board::score_lut     = board::build_score_lut();

int main()
{
}

